from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    entrerprise = models.BooleanField(default=False)
    particulier = models.BooleanField(default=True)
    nom_entreprise = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=10)
    photo_profil = models.ImageField(upload_to="profile_pictures")

    def __str__(self):
        return self.username