from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from transaction.models import Compte

User = get_user_model()

class ObjectifFinancier(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    motif = models.CharField(max_length=200)
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    montant_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, null=True, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    STATUT = (
        ("En cours", "En cours"),
        ("Atteint", "Atteint"),
        ("Non atteint", "Non atteint")
    )
    statut = models.CharField(max_length=20, choices=STATUT, default="En cours")

    def __str__(self):
        return f"{self.utilisateur.username} : {self.objectif}"
    
    def save(self, *args, **kwargs):
        if self.montant_actuel == self.objectif:
            self.statut = "Atteint"
        return super().save(*args, **kwargs)
    
    @classmethod
    def total(cls, user):
        return cls.objects.filter(utilisateur=user).count()

    @classmethod
    def atteint(cls, user):
        return cls.objects.filter(utilisateur=user, statut="Atteint").count()


class ChargeMensuelle(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type_charge = models.CharField(max_length=255)
    etat = models.BooleanField(default=False)  # False = non payé, True = payé
    date_paiement = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.utilisateur.username} : {self.montant} - {self.type_charge}"
