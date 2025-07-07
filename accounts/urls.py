from django.urls import path, include
from django.contrib import admin
from . import  views 


urlpatterns = [
    path('accounts/', views.all_accounts,),
    path('login/', views.login_page , name='login'),  
    path('rh/', views.rh_page, name='rh_page'),  
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('evaluate_employe/<int:user_id>/', views.evaluate_employe, name='evaluate_employe'),
    path('employe/', views.employe_page, name='employe_page'),
    path('postuler-conge/', views.postuler_conge, name='postuler_conge'),
    path('valider-tache/<int:tache_id>/', views.valider_tache, name='valider_tache'),
    path('admin_dashboard/', views.admin_page, name='admin_dashboard'),
    path('manager/', views.manager_page, name='manager_page'),
    path('valider-conge/<int:demande_id>/', views.valider_conge, name='valider_conge'),
    path('notifier-employe-conge/<int:demande_id>/', views.notifier_employe_conge, name='notifier_employe_conge'),
    path('assigner-tache/', views.assigner_tache, name='assigner_tache'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),  

]