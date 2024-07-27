from calendar import month_name
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from transaction.models import Transaction, Compte, Categorie
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta
from django.db.models import Sum

from dashboard.paticulier import CalculDepenseParticulierUsd, CalculDepenseParticulierCdf
from dashboard.paticulier import CalculGainParticulierUsd, CalculGainParticulierCdf
from dashboard.paticulier import CalculTotalSoldeUserCdf, CalculTotalSoldeUserUsd

from django.db.models import Sum


User = get_user_model()

def get_revenues_by_category(request):
    today = datetime.today()
    debut_mois = today.replace(day=1)
    fin_mois = today.replace(day=1, month=today.month + 1) - timedelta(days=1)

    # Filter transactions for Credits (revenues) within the month
    transactions = Transaction.objects.filter(
        date_transaction__range=(debut_mois, fin_mois),
        type_transaction="Débit",
        utilisateur=request.user
    ).values('categorie__nom_categorie') \
      .annotate(total=Sum('montant'))  # Group by category and sum amount

    # Return dictionary with category names and total revenues
    return {transaction['categorie__nom_categorie']: transaction['total'] for transaction in transactions}

def get_depenses_by_category(request):
    today = datetime.today()
    debut_mois = today.replace(day=1)
    fin_mois = today.replace(day=1, month=today.month + 1) - timedelta(days=1)

    # Filter transactions for Debits (expenses) within the month
    transactions = Transaction.objects.filter(
        date_transaction__range=(debut_mois, fin_mois),
        type_transaction="Crédit",
        utilisateur=request.user
    ).values('categorie__nom_categorie') \
      .annotate(total=Sum('montant'))  # Group by category and sum amount

    # Return dictionary with category names and total expenses
    return {transaction['categorie__nom_categorie']: transaction['total'] for transaction in transactions}


def budgetGenere(request):
    today = datetime.today()
    debut_mois = today.replace(day=1)
    fin_mois = today.replace(day=1, month=today.month + 1) - timedelta(days=1)

    # Filtrer les transactions pour les dépenses du mois en cours
    transactions_depenses = Transaction.objects.filter(
        date_transaction__range=(debut_mois, fin_mois),
        type_transaction="Crédit",
        utilisateur=request.user
    ).values('categorie__nom_categorie') \
      .annotate(total=Sum('montant'))  # Regrouper par catégorie et sommer les montants

    # Filtrer les transactions pour les revenus du mois en cours
    transactions_revenus = Transaction.objects.filter(
        date_transaction__range=(debut_mois, fin_mois),
        type_transaction="Débit",
        utilisateur=request.user
    ).values('categorie__nom_categorie') \
      .annotate(total=Sum('montant'))  # Regrouper par catégorie et sommer les montants

    # Récupérer les noms de catégorie et les montants totaux
    depenses = {transaction['categorie__nom_categorie']: transaction['total'] for transaction in transactions_depenses}
    revenus = {transaction['categorie__nom_categorie']: transaction['total'] for transaction in transactions_revenus}

    # Récupérer le nom du mois en cours
    current_month = month_name[today.month]

    # Préparer les données pour le rendu
    data = []
    for categorie in Categorie.objects.filter(user=request.user):
        montant_budgete = categorie.limite
        montant_depenses = depenses.get(categorie.nom_categorie, 0)
        montant_revenus = revenus.get(categorie.nom_categorie, 0)

        ecartDepenses = montant_budgete - montant_depenses
        ecartRevenus = montant_budgete - montant_revenus

        data.append({
            'categorie': categorie.nom_categorie,
            'montant_budgete': montant_budgete,
            'montant_depenses': montant_depenses,
            'montant_revenus': montant_revenus,
            'ecartDepenses': ecartDepenses,
            'ecartRevenus': ecartRevenus,
            'date_depense': fin_mois if montant_depenses > 0 else '',  # Date de dépense vide pour les revenus
            'mode_paiement': Compte.objects.filter(proprietaire=request.user).first().operateur,  # Vous pouvez ajuster cela
            'mois_en_cours': current_month,
            'type_transaction': 'Dépense' if montant_depenses > 0 else 'Revenu',
        })

    return data


@login_required
def all_expense(request):
    expenses = get_depenses_by_category(request)
    label_expenses = []
    data_expenses = []
    for expense in expenses:
        label_expenses.append(expense)
        data_expenses.append(float(expenses[expense]))

    gains = get_revenues_by_category(request)
    label_gains = []
    data_gains = []
    for gain in gains:
        label_gains.append(gain)
        data_gains.append(float(gains[gain]))

    budget_mensuel = budgetGenere(request)


    return render(request, "analyse/all_expenses.html", {
        "label_expenses": label_expenses,
        "data_expenses": data_expenses,
        "label_gains": label_gains,
        "data_gains": data_gains,
        "budget_mensuel": budget_mensuel,

        "somme_total_usd": CalculTotalSoldeUserUsd(request),
        "somme_total_cdf": CalculTotalSoldeUserCdf(request),
        "gainParticulierUsd" : CalculGainParticulierUsd(request),
        "depenseParticulierUsd" : CalculDepenseParticulierUsd(request),
        "gainParticulierCdf" : CalculGainParticulierCdf(request),
        "depenseParticulierCdf": CalculDepenseParticulierCdf(request),
    })

@login_required
def generate_user_budget(request):
    # Get the user object
    user = request.user

    # Obtenir la date actuelle
    date_actuelle = date.today()

    # Extraire l'année et le mois actuels
    annee, mois = date_actuelle.year, date_actuelle.month

    # Filtrer les transactions pour l'utilisateur, le mois et l'année actuels
    transactions = Transaction.objects.filter(
        utilisateur=user,
        date_transaction__year=annee,
        date_transaction__month=mois,
        date_transaction__lte=date_actuelle
    )

    # Créer un dictionnaire pour stocker les totaux par catégorie
    categories_budget = {}

    # Itérer sur les transactions et accumuler les dépenses par catégorie
    for transaction in transactions:
        nom_categorie = transaction.categorie.nom_categorie
        montant = transaction.montant

        if nom_categorie in categories_budget:
            categories_budget[nom_categorie] += montant
        else:
            categories_budget[nom_categorie] = montant

    print(categories_budget)

    # Rendre le modèle de budget avec les données générées
    context = {
        'year': annee,
        'month': mois,
        'budget': categories_budget,
    }
    return render(request, 'budget/budget.html', context)

