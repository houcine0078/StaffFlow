from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Message, Tache, Utilisateur, Demande
from django.contrib.auth.decorators import login_required

def all_accounts(request):
    return HttpResponse('Return all accounts')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'ADMIN': # type: ignore
                    return redirect('/admin/')
                elif user.role == 'RH': # type: ignore
                    return redirect('rh_page')
                elif user.role == 'MANAGER': # type: ignore
                    return redirect('manager_page')
                elif user.role == 'EMPLOYE': # type: ignore
                    return redirect('employe_page')
                else:
                    messages.error(request, "Rôle invalide.")
                    return redirect('login')
            else:
                messages.error(request, "Mot de passe incorrect.")
                return redirect('login')
        except Utilisateur.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé.")
            return redirect('login')
    return render(request, 'LoginPage.html')

@login_required
def admin_page(request):
    if request.user.role != 'ADMIN':
        return redirect('login')
    return render(request, '/admin/')

@login_required
def rh_page(request):
    if request.user.role != 'RH':
        return redirect('login')
    users = Utilisateur.objects.exclude(role='ADMIN').exclude(role='RH').exclude(id=request.user.id)
    # On récupère les demandes validées ou refusées par le manager
    demandes_conge = Demande.objects.filter(statut__in=['APPROUVEE', 'REFUSEE'])
    return render(request, 'RhPage.html', {
        'users': users,
        'current_user': request.user,
        'demandes_conge': demandes_conge,
    })

@login_required
def send_message(request, user_id):
    destinataire = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST':
        sujet = request.POST.get('sujet', '')
        contenu = request.POST.get('contenu', '')
        if contenu:
            Message.objects.create(
                expediteur=request.user,
                destinataire=destinataire,
                sujet=sujet,
                contenu=contenu
            )
        return redirect('rh_page')
    return HttpResponse(status=405)

@login_required
def evaluate_employe(request, user_id):
    employe = get_object_or_404(Utilisateur, id=user_id, role='EMPLOYE')
    if request.method == 'POST':
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        # À adapter selon ton modèle d'évaluation
        employe.note = note # type: ignore
        employe.commentaire = commentaire # type: ignore
        employe.save()
        return redirect('rh_page')
    return render(request, 'Evaluer_Employe.html', {'employe': employe})

@login_required
def manager_page(request):
    if request.user.role != 'MANAGER':
        return redirect('login')
    equipe = Utilisateur.objects.filter(manager=request.user, role='EMPLOYE')
    taches = Tache.objects.filter(cree_par=request.user)
    demandes_conge = Demande.objects.filter(employe__manager=request.user)
    return render(request, 'ManagerPage.html', {
        'current_user': request.user,
        'equipe': equipe,
        'taches': taches,
        'demandes_conge': demandes_conge,
    })

@login_required
def assigner_tache(request):
    if request.user.role != 'MANAGER':
        return redirect('login')
    if request.method == 'POST':
        employe_id = request.POST.get('employe')
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        date_echeance = request.POST.get('date_echeance')
        if employe_id and titre and description and date_echeance:
            employe = Utilisateur.objects.get(id=employe_id)
            Tache.objects.create(
                employe=employe,
                titre=titre,
                description=description,
                date_echeance=date_echeance,
                cree_par=request.user
            )
    return redirect('manager_page')

@login_required
def employe_page(request):
    if request.user.role != 'EMPLOYE':
        return redirect('login')
    messages_recus = Message.objects.filter(destinataire=request.user).order_by('-date_envoi')
    demandes_conge = Demande.objects.filter(employe=request.user).order_by('-date_debut')
    taches_assignees = Tache.objects.filter(employe=request.user)
    return render(request, 'EmployePage.html', {
        'current_user': request.user,
        'messages_recus': messages_recus,
        'demandes_conge': demandes_conge,
        'taches_assignees': taches_assignees,
    })

@login_required
def valider_tache(request, tache_id):
    tache = get_object_or_404(Tache, id=tache_id, employe=request.user)
    if request.method == 'POST':
        tache.est_terminee = True
        tache.save()
    return redirect('employe_page')

@login_required
def postuler_conge(request):
    if request.user.role != 'EMPLOYE':
        return redirect('login')
    if request.method == 'POST':
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        motif = request.POST.get('motif')
        if date_debut and date_fin and motif:
            Demande.objects.create(
                employe=request.user,
                date_debut=date_debut,
                date_fin=date_fin,
                motif=motif,
                statut='EN_ATTENTE'
            )
    return redirect('employe_page')


@login_required
def valider_conge(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'valider':
            demande.statut = 'APPROUVEE'
            decision = "acceptée"
        elif action == 'refuser':
            demande.statut = 'REFUSEE'
            decision = "refusée"
        else:
            decision = "traitée"
        demande.save()
        # Notifier le RH
        rh_users = Utilisateur.objects.filter(role='RH')
        for rh in rh_users:
            Message.objects.create(
                expediteur=request.user,
                destinataire=rh,
                sujet="Demande de congé à traiter",
                contenu=f"La demande de congé de {demande.employe.get_full_name()} a été {decision} par le manager. Merci de notifier l'employé."
            )
    return redirect('manager_page')

@login_required
def notifier_employe_conge(request, demande_id):
    if request.user.role != 'RH':
        return redirect('login')
    demande = get_object_or_404(Demande, id=demande_id)
    if request.method == 'POST':
        Message.objects.create(
            expediteur=request.user,
            destinataire=demande.employe,
            sujet="Réponse à votre demande de congé",
            contenu=f"Votre demande de congé a été {demande.get_statut_display().lower()}." # type: ignore
        )
    return redirect('rh_page')

def logout_view(request):
    logout(request)
    return redirect('login')

def custom_admin_logout(request):
    logout(request)
    return redirect('login')

@login_required
def update_profile(request):
    if request.method == 'POST':
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        user = request.user
        user.telephone = telephone
        user.adresse = adresse
        user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))