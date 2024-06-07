from django.db import models

class Album(models.Model):
    titre = models.CharField(max_length=200)
    artiste = models.CharField(max_length=200)
    date_production = models.DateField()
    nb_piste = models.IntegerField()
    minute = models.IntegerField()

    def __str__(self):
        return self.titre

    def __repr__(self):
        return f"<Album (titre={self.titre}, artiste={self.artiste}, date_production={self.date_production}, nb_piste={self.nb_piste}, minute={self.minute})>"

    def get_duration(self):
        hours = self.minute // 60
        minutes = self.minute % 60
        return f"{hours}h:{minutes}m"