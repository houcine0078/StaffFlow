from django.contrib.auth.models import AbstractUser 
from typing import List, Tuple

#c'est une classe avec les attributs standard 
#Django crée automatiquement un id et les autre attributs comme username,... sont importé de cette classe
#on peut ajouter des attributs 

from django.db import models

#--- modèle utilisateur ----

class Utilisateur(AbstractUser): 

    email = models.EmailField(unique=True)

    #On crér la classe  
    # #ROLE_Choices est liste de choix possible pour le champ role , c'est comme ENUM dans la base de données
    
    ROLE_CHOICES = [   
        ('ADMIN', 'Administrateur'),
        ('RH', 'Ressources Humaines'),
        ('MANAGER', 'Manager'),
        ('EMPLOYE', 'Employé'),
    ] 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES) #On créer les champs 
    telephone = models.CharField(max_length=20, blank=True)#On doit obligatoirement définire une longeur max pour charField comme varchar()
    adresse = models.TextField(blank=True)
    date_embauche = models.DateField(null=True, blank=True)

    # Chaque employé peut avoir un manager. Un manager peut avoir plusieurs employés.
    # manager est un champs de plus qui permet de créer une relations entre les utilisateurs 
    
    manager = models.ForeignKey(
        'self',  # relation vers un autre utilisateur
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'MANAGER'},  # ne permettre que les utilisateurs avec rôle 'MANAGER'
        related_name='equipe'  # pour récupere tous les utilisateurs qui ont le meme manager.equipe.all()
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # or add other required fields if needed


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    


    #---- modèle demande -----


class Demande(models.Model) :        
 TYPE_CHOICES: List[Tuple[str, str]] = [
       ('CONGE', 'Demande de congé'),
       ('ATTESTATION', 'Demande d’attestation'),
       ('AUTRE', 'Autre'),
    ]
    
 STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVEE', 'Approuvée'),
        ('REFUSEE', 'Refusée'),
    ]

 employe = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, limit_choices_to={'role': 'EMPLOYE'})
 type_demande = models.CharField(max_length=20, choices=TYPE_CHOICES)
 statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
 date_demande = models.DateTimeField(auto_now_add=True)
 message = models.TextField(blank=True)
 message_traitement = models.TextField(blank=True)
 date_debut = models.DateField(null=True, blank=True)
 date_fin = models.DateField(null=True, blank=True)
 motif = models.TextField(null=True, blank=True)


def __str__(self):
        return f"{self.get_type_demande_display()} - {self.employe.username}"
    

    #--- modèle message----

class Message(models.Model):
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_recus')
    sujet = models.CharField(max_length=100)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.expediteur.username} à {self.destinataire.username} - {self.sujet}"

#-----modèle tache ----


class Tache(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_echeance = models.DateField(null=True, blank=True)
    est_terminee = models.BooleanField(default=False)

    employe = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, limit_choices_to={'role': 'EMPLOYE'})
    cree_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'MANAGER'}, related_name='taches_creees')

    def __str__(self):
        return f"{self.titre} - {self.employe.username}"

#----modèle contrat ----

class Contrat(models.Model):
    employe = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, limit_choices_to={'role': 'EMPLOYE'})
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    type_contrat = models.CharField(max_length=50)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Contrat de {self.employe.username} - {self.type_contrat}"


