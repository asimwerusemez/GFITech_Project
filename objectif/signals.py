from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import Compte
from .models import ObjectifFinancier

@receiver(post_save, sender=ObjectifFinancier)
def update_account_balance_particulier(sender, instance, created, **kwargs):
    if created:
        instance.compte.solde -= instance.montant_actuel
        instance.compte.save()

