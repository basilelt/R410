from rest_framework import serializers
from .models import Album

class AlbumSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ["titre", "artiste", "date_production", "nb_piste", "minute", "duration"]

    def get_duration(self, obj):
        return obj.get_duration()