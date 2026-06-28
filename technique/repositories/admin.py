from django.contrib import admin
from .models import Repository, Fichier


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['nom', 'created_at']
    search_fields = ['nom']


@admin.register(Fichier)
class FichierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'repository', 'type_fichier', 'langage', 'est_critique']
    list_filter = ['est_critique', 'type_fichier', 'langage']
    search_fields = ['nom']