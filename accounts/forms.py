#les formulaires servent à gérer la saisie de données par l'utilisateur dans des pages HTML

from django import forms
from .models import Demande, Message, Tache, Contrat

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        fields = ['employe', 'type_demande', 'statut', 'message_traitement']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['expediteur', 'destinataire', 'contenu']

class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['titre', 'description', 'date_echeance', 'statut']

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = ['employe', 'date_debut', 'date_fin', 'type_contrat']
