from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Repository, Fichier
from .serializers import (
    RepositorySerializer,
    RepositoryDetailSerializer,
    FichierSerializer,
)


class ListeRepositories(generics.ListCreateAPIView):
    """
    GET  -> liste tous les repositories
    POST -> crée un nouveau repository
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class DetailRepository(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    -> detail d'un repository avec ses fichiers
    PUT    -> modifier
    DELETE -> supprimer
    """
    queryset = Repository.objects.all()

    def get_serializer_class(self):
        # pour le GET on veut les fichiers, pour PUT non
        if self.request.method == 'GET':
            return RepositoryDetailSerializer
        return RepositorySerializer


class FichiersRepository(generics.ListCreateAPIView):
    """
    GET  -> liste les fichiers d'un repository
    POST -> ajoute un fichier a un repository
    """
    serializer_class = FichierSerializer

    def get_queryset(self):
        repo_id = self.kwargs['pk']
        return Fichier.objects.filter(repository_id=repo_id)

    def perform_create(self, serializer):
        repo = get_object_or_404(Repository, pk=self.kwargs['pk'])
        serializer.save(repository=repo)


class RechercheFichiers(APIView):
    """
    Recherche de fichiers par nom, langage ou type
    exemples:
      GET /api/fichiers/?nom=settings
      GET /api/fichiers/?langage=Python
      GET /api/fichiers/?type=config
    """

    def get(self, request):
        fichiers = Fichier.objects.all()

        nom = request.query_params.get('nom')
        langage = request.query_params.get('langage')
        type_f = request.query_params.get('type')

        if nom:
            fichiers = fichiers.filter(nom__icontains=nom)
        if langage:
            fichiers = fichiers.filter(langage__icontains=langage)
        if type_f:
            fichiers = fichiers.filter(type_fichier__icontains=type_f)

        serializer = FichierSerializer(fichiers, many=True)
        return Response(serializer.data)


class FichiersCritiques(generics.ListAPIView):
    """
    GET -> retourne tous les fichiers marques comme critiques
    """
    serializer_class = FichierSerializer

    def get_queryset(self):
        return Fichier.objects.filter(est_critique=True)