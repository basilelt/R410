from django.db import models

# Create your models here.

class Client(models.Model):
    genre = models.CharField(max_length=20, null=True, blank=True)
    nom = models.CharField(max_length=100, null=False, blank=False)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    identifiant = models.CharField(max_length=200, null=False, blank=False, unique=True)
    mot_de_passe = models.CharField(max_length=200, null=False, blank=False)
    adresse = models.TextField(null=True, blank=True)
    mail = models.CharField(max_length=256, null=False, blank=False)
    telephone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.identifiant

    def __repr__(self):
        return f"<Client (identifiant={self.identifiant}, nom={self.nom}, mail={self.mail})>"