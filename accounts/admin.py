from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    # Ajoute 'manager' dans les champs affichés et éditables
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'manager', 'telephone', 'adresse', 'date_embauche',)}),
    ) # type: ignore
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'manager', 'telephone', 'adresse', 'date_embauche',)}),
    )
    list_display = UserAdmin.list_display + ('role', 'manager', 'telephone', 'adresse', 'date_embauche') # type: ignore

admin.site.register(Utilisateur, UtilisateurAdmin)