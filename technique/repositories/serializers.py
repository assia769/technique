from rest_framework import serializers
from .models import Repository, Fichier
from .services import fichier_est_critique


class FichierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fichier
        fields = [
            'id',
            'nom',
            'chemin',
            'type_fichier',
            'langage',
            'taille',
            'description',
            'date_ajout',
            'est_critique',
        ]
        # est_critique est en lecture seule, c'est calcule automatiquement
        read_only_fields = ['est_critique', 'date_ajout']

    def create(self, validated_data):
        # on cree le fichier puis on calcule si il est critique
        fichier = Fichier(**validated_data)
        fichier.est_critique = fichier_est_critique(fichier)
        fichier.save()
        return fichier


class RepositorySerializer(serializers.ModelSerializer):
    # juste le nombre de fichiers, pas la liste complete
    nombre_fichiers = serializers.IntegerField(
        source='fichiers.count',
        read_only=True
    )

    class Meta:
        model = Repository
        fields = ['id', 'nom', 'description', 'created_at', 'nombre_fichiers']
        read_only_fields = ['created_at']


class RepositoryDetailSerializer(serializers.ModelSerializer):
    # pour le detail on inclut tous les fichiers
    fichiers = FichierSerializer(many=True, read_only=True)

    class Meta:
        model = Repository
        fields = ['id', 'nom', 'description', 'created_at', 'updated_at', 'fichiers']
        read_only_fields = ['created_at', 'updated_at']