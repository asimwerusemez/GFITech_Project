from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Compte(models.Model):
    """Modèle pour les comptes financiers."""

    DEVISE = (
        ("CDF", "CDF"),
        ("USD", "USD")
    )

    OPERATEUR = (
        ("Mpesa", "Mpesa"),
        ("Airtel Money", "Airtel Money"),
        ("Orange Money", "Orange Money"),
        ("Equity Bank", "Equity Bank"),
        ("RawBank", "RawBank"),
        ("Caisse", "Caisse")
    )

    nom_compte = models.CharField(max_length=50, null=True, blank=True)
    operateur = models.CharField(max_length=50, choices=OPERATEUR, default="Caisse", null=True, blank=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    devise = models.CharField(max_length=5, choices=DEVISE)
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_compte or self.operateur


class Categorie(models.Model):
    nom_categorie = models.CharField(max_length=50)
    limite = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description_categorie = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.nom_categorie

class Alert(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    nom_categorie = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    TYPE_TRANS = (
        ("Débit", "Débit"),
        ("Crédit", "Crédit")
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=10, choices=TYPE_TRANS)
    date_transaction = models.DateField()
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)  # Assurez-vous d'importer Compte si nécessaire
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.utilisateur.username} - {self.categorie.nom_categorie} : {self.montant}"


class File(models.Model):
    file = models.FileField(upload_to="fichiers")
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, blank=True, null=True)

    