from django.views.generic import TemplateView
from django.db.models import Sum, Q
from transaction.models import Compte, Categorie, Transaction
from datetime import datetime

class BudgetVue(TemplateView):
    template_name = "budget/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Solde des comptes
        comptes = Compte.objects.filter(proprietaire=user)
        context['comptes'] = comptes

        # Dépenses par catégorie
        date_debut = self.request.GET.get('date_debut')
        date_fin = self.request.GET.get('date_fin')

        if date_debut and date_fin:
            date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
            date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()
        else:
            date_debut = None
            date_fin = None

        transactions = Transaction.objects.filter(Q(compte__proprietaire=user) & Q(date_transaction__gte=date_debut) & Q(date_transaction__lte=date_fin))
        depenses_par_categorie = transactions.filter(type_transaction='Débit').values('categorie__nom_categorie').annotate(montant=Sum('montant'))
        context['depenses_par_categorie'] = depenses_par_categorie

        # Revenus totaux
        revenus_totaux = transactions.filter(type_transaction='Crédit').aggregate(Sum('montant'))['montant__sum'] or 0
        context['revenus_totaux'] = revenus_totaux

        # Dépenses totales
        depenses_totales = transactions.filter(type_transaction='Débit').aggregate(Sum('montant'))['montant__sum'] or 0
        context['depenses_totales'] = depenses_totales

        # Budgets
        budgets = Categorie.objects.filter(user=user)
        context['budgets'] = budgets

        return context
