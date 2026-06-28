from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Repository, Fichier
from .services import fichier_est_critique


class TestServiceCritique(TestCase):
    """tests pour la logique de detection des fichiers critiques"""

    def setUp(self):
        self.repo = Repository.objects.create(
            nom='Repo de test',
            description='pour les tests'
        )

    def test_fichier_sans_description_est_critique(self):
        f = Fichier(
            repository=self.repo,
            nom='main.py',
            chemin='main.py',
            type_fichier='source',
            taille=100,
            description=''
        )
        self.assertTrue(fichier_est_critique(f))

    def test_fichier_trop_grand_est_critique(self):
        f = Fichier(
            repository=self.repo,
            nom='dump.sql',
            chemin='dump.sql',
            type_fichier='autre',
            taille=6 * 1024 * 1024,  # 6 Mo
            description='dump de la base'
        )
        self.assertTrue(fichier_est_critique(f))

    def test_fichier_env_est_critique(self):
        f = Fichier(
            repository=self.repo,
            nom='.env',
            chemin='.env',
            type_fichier='config',
            taille=200,
            description='variables d environnement'
        )
        self.assertTrue(fichier_est_critique(f))

    def test_fichier_normal_pas_critique(self):
        f = Fichier(
            repository=self.repo,
            nom='utils.py',
            chemin='app/utils.py',
            type_fichier='source',
            taille=1500,
            description='fonctions utilitaires du projet'
        )
        self.assertFalse(fichier_est_critique(f))


class TestAPIRepositories(APITestCase):
    """tests des endpoints API"""

    def test_creer_repository(self):
        data = {'nom': 'Mon projet', 'description': 'projet de test'}
        response = self.client.post('/api/repositories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repository.objects.count(), 1)

    def test_lister_repositories(self):
        Repository.objects.create(nom='Repo1', description='desc')
        Repository.objects.create(nom='Repo2', description='desc')
        response = self.client.get('/api/repositories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_repository(self):
        repo = Repository.objects.create(nom='Repo test', description='desc')
        response = self.client.get(f'/api/repositories/{repo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nom'], 'Repo test')

    def test_ajouter_fichier(self):
        repo = Repository.objects.create(nom='Repo', description='desc')
        data = {
            'nom': 'settings.py',
            'chemin': 'config/settings.py',
            'type_fichier': 'config',
            'langage': 'Python',
            'taille': 3000,
            'description': 'configuration principale'
        }
        response = self.client.post(f'/api/repositories/{repo.id}/fichiers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recherche_par_langage(self):
        repo = Repository.objects.create(nom='Repo', description='desc')
        Fichier.objects.create(
            repository=repo, nom='app.py', chemin='app.py',
            type_fichier='source', langage='Python', taille=500,
            description='point d entree'
        )
        response = self.client.get('/api/fichiers/?langage=Python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fichiers_critiques(self):
        repo = Repository.objects.create(nom='Repo', description='desc')
        # ce fichier sera critique (pas de description)
        Fichier.objects.create(
            repository=repo, nom='secret.key', chemin='secret.key',
            type_fichier='config', langage='', taille=100,
            description='', est_critique=True
        )
        response = self.client.get('/api/fichiers/critiques/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)