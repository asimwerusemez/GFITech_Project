from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import Categorie, Transaction, Alert

@receiver(post_save, sender=Transaction)
def update_account_balance_particulier(sender, instance, created, **kwargs):
    if created:
        if (float(instance.montant) > float(instance.categorie.limite)) and instance.type_transaction == "Crédit":
            alert = Alert.objects.create(
                montant=instance.montant - instance.categorie.limite,
                nom_categorie=f"Dépassement du montant dans la catégorie {instance.categorie.nom_categorie}",
                user=instance.utilisateur
            )
            
        elif (float(instance.montant) < float(instance.categorie.limite)) and instance.type_transaction == "Débit":
            alert = Alert.objects.create(
                montant=instance.montant - instance.categorie.limite,
                nom_categorie=f"insuffisance du montant dans la catégorie {instance.categorie.nom_categorie}",
                user=instance.utilisateur
            )
