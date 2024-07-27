from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay

from transaction.models import Compte, Transaction, Categorie
from objectif.models import ObjectifFinancier


def CalculTotalSoldeUserUsd(request):
    comptes = Compte.objects.filter(proprietaire=request.user)

    # Calculer le total des soldes en USD et CDF de manière efficace
    somme_total_usd = comptes.filter(devise="USD").aggregate(solde_sum=Sum("solde"))["solde_sum"] or 0

    return somme_total_usd

def CalculTotalSoldeUserCdf(request):
    # Obtenir les comptes de l'utilisateur
    comptes = Compte.objects.filter(proprietaire=request.user)
    somme_total_cdf = comptes.filter(devise="CDF").aggregate(solde_sum=Sum("solde"))["solde_sum"] or 0

    return somme_total_cdf

def CalculDepenseParticulierUsd(request):
    depenseParticulierUsd = Transaction.objects.filter(utilisateur=request.user, type_transaction="Crédit", compte__devise="USD").aggregate(montant_sum=Sum("montant"))["montant_sum"] or 0

    return depenseParticulierUsd

def CalculDepenseParticulierCdf(request):
    depenseParticulierCdf = Transaction.objects.filter(utilisateur=request.user, type_transaction="Crédit", compte__devise="CDF").aggregate(montant_sum=Sum("montant"))["montant_sum"] or 0

    return depenseParticulierCdf

def CalculGainParticulierUsd(request):
    gainParticulier = Transaction.objects.filter(utilisateur=request.user, type_transaction="Débit", compte__devise="USD").aggregate(montant_sum=Sum("montant"))["montant_sum"] or 0

    totalGain = (gainParticulier + CalculDepenseParticulierUsd(request)) - CalculTotalSoldeUserUsd(request)

    if totalGain < 0:
        return abs(totalGain) + (gainParticulier)
    else:
        newTotal = totalGain + CalculDepenseParticulierUsd(request)
        return abs(newTotal)

def CalculGainParticulierCdf(request):
    gainParticulier = Transaction.objects.filter(utilisateur=request.user, type_transaction="Débit", compte__devise="CDF").aggregate(montant_sum=Sum("montant"))["montant_sum"] or 0

    totalGain = (gainParticulier + CalculDepenseParticulierCdf(request)) - CalculTotalSoldeUserCdf(request)

    if totalGain < 0:
        return abs(totalGain) + (gainParticulier)
    else:
        newTotal = totalGain + CalculDepenseParticulierCdf(request)
        return abs(newTotal)
    
def last_transactions(request):
    # Récupérer les 5 dernières transactions de l'utilisateur connecté
    transactions = Transaction.objects.filter(utilisateur=request.user).order_by('-date_transaction')[:5]
    return transactions

def gains_view(request):
    # Gains mensuels
    gains_mensuels = Transaction.objects.filter(utilisateur=request.user, type_transaction="Crédit").annotate(month=TruncMonth('date_transaction')).values('month').annotate(total=Sum('montant')).order_by('month')

    labels = [gain['month'].strftime('%B') for gain in gains_mensuels]  # Afficher le nom du mois
    data = [float(gain['total']) for gain in gains_mensuels]

    return {"labels": labels, "data": data}

def totalObjectifMontant(request):
    montant_objectif = ObjectifFinancier.objects.filter(utilisateur=request.user).aggregate(montant_actuel_sum=Sum("montant_actuel"))["montant_actuel_sum"] or 0

    return montant_objectif

def receive_user(request):
    reception = Transaction.objects.filter(utilisateur=request.user, type_transaction="Débit").order_by("-montant")[:3]

    return reception

def charge_mensuelle(request):
    charges = Transaction.objects.filter(utilisateur=request.user, type_transaction="Crédit").order_by("-montant")[:2]

    return charges
