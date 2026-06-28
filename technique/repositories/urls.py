from django.urls import path
from . import views

urlpatterns = [
    path('repositories/', views.ListeRepositories.as_view(), name='liste-repositories'),
    path('repositories/<int:pk>/', views.DetailRepository.as_view(), name='detail-repository'),
    path('repositories/<int:pk>/fichiers/', views.FichiersRepository.as_view(), name='fichiers-repository'),
    path('fichiers/', views.RechercheFichiers.as_view(), name='recherche-fichiers'),
    path('fichiers/critiques/', views.FichiersCritiques.as_view(), name='fichiers-critiques'),
]