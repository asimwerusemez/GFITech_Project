from django.db import models

class Contact(models.Model):
    nom = models.CharField(max_length=30)
    email =  models.EmailField()
    phone =  models.CharField(max_length=14)
    message = models.TextField()
    particulier = models.BooleanField(default=False)
    entreprise = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.nom} - {self.phone}"
