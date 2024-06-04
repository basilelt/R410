from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["genre", "nom", "prenom", "identifiant", "mot_de_passe", "adresse", "mail", "telephone"]