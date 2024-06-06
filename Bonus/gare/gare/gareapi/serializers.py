from rest_framework import serializers
from .models import Gare

class GareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gare
        fields = ["nom", "ville", "code_postal", "nb_quais", "date_construction"]