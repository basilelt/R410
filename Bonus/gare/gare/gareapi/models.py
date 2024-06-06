from django.db import models

class Gare(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=5, )
    nb_quais = models.IntegerField()
    date_construction = models.DateTimeField()

    def __str__(self):
        return self.nom

    def __repr__(self):
        return f"<Gare (nom={self.nom}, ville={self.ville}, code_postal={self.code_postal}, nb_quais={self.nb_quais}, date_construction={self.date_construction})>"
    