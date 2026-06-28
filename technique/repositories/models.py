from django.db import models


class Repository(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['-created_at']


class Fichier(models.Model):
    # types de fichiers qu'on peut rencontrer dans un repo
    TYPE_CHOICES = [
        ('source', 'Source'),
        ('config', 'Configuration'),
        ('doc', 'Documentation'),
        ('test', 'Test'),
        ('autre', 'Autre'),
    ]

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name='fichiers'
    )
    nom = models.CharField(max_length=255)
    chemin = models.CharField(max_length=500)
    type_fichier = models.CharField(max_length=50, choices=TYPE_CHOICES, default='source')
    langage = models.CharField(max_length=100, blank=True, default='')
    # taille en octets
    taille = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, default='')
    date_ajout = models.DateTimeField(auto_now_add=True)
    # ce champ est calculé automatiquement a la creation
    est_critique = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} ({self.repository.nom})"

    class Meta:
        ordering = ['-date_ajout']