from django.db import models

# Create your models here.

class Commentaire(models.Model):
    titre = models.CharField(max_length=200)
    commentaire = models.TextField()
    date_de_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    def __repr__(self):
        return f"<Commentaire (titre={self.titre}, date_de_publication={self.date_de_publication})>"