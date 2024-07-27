from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import Compte, Transaction

@receiver(post_save, sender=Transaction)
def update_account_balance_particulier(sender, instance, created, **kwargs):
    if created:
        if instance.type_transaction == "Débit":
            instance.compte.solde += int(instance.montant)
            instance.compte.save()
        elif instance.type_transaction == "Crédit":
            instance.compte.solde -= int(instance.montant)
            instance.compte.save()