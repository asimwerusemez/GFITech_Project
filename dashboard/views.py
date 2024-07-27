from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



from transaction.models import Compte, Transaction, Categorie
from .paticulier import *

def compteUser(request):
    # Obtenir les comptes de l'utilisateur
    comptes = Compte.objects.filter(proprietaire=request.user)
    return comptes


@login_required
def view_dash(request):

    transactions = Transaction.objects.filter(utilisateur=request.user, type_transaction="Crédit").order_by('-date_transaction')[:5]

    # Gains mensuels
    gains_mensuels = Transaction.objects.filter(utilisateur=request.user, type_transaction="Débit").annotate(month=TruncMonth('date_transaction')).values('month').annotate(total=Sum('montant')).order_by('month')

    labels = [gain['month'].strftime('%B') for gain in gains_mensuels]  # Afficher le nom du mois
    data = [float(gain['total']) for gain in gains_mensuels]


    # creation de progress bar pour les objectifs
    total_objectif = ObjectifFinancier.total(request.user) or 0
    atteint_objectif = ObjectifFinancier.atteint(request.user) or 0

    contexte = {
        "comptes": compteUser(request),
        "somme_total_usd": CalculTotalSoldeUserUsd(request),
        "somme_total_cdf": CalculTotalSoldeUserCdf(request),
        "gainParticulierUsd" : CalculGainParticulierUsd(request),
        "depenseParticulierUsd" : CalculDepenseParticulierUsd(request),
        "gainParticulierCdf" : CalculGainParticulierCdf(request),
        "depenseParticulierCdf": CalculDepenseParticulierCdf(request),

        # afficher 5 dernières transaction particulier
        "transactions" : transactions,
        # gain Mensuel
        "labels": labels,
        "data": data,

        # graphique pour comparer le motant actuel objectif et gain total
        "montant_objectf": totalObjectifMontant(request),

        # progress bar pour les objectifs
        "total": total_objectif,
        "atteint": atteint_objectif,

        # entrer d'argents
        "receptions": receive_user(request),
        #charges mensuelle
        "charges_mensuelles": charge_mensuelle(request)

    }

    return render(request, "dashboard/dashboard.html", contexte)


def gain_view(request):
    return render(request, "dashboard/test.html", {})