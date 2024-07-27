from django import forms
from .models import Compte, File, Transaction, Categorie


class AddCompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ("operateur", "solde", "devise")

class FileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FileForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['compte'].queryset = Compte.objects.filter(proprietaire=user)

    class Meta:
        model = File
        fields = ['file', 'compte']

class TransactionForm(forms.ModelForm):
    date_transaction = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-cat1'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['compte'].queryset = Compte.objects.filter(proprietaire=user)

    class Meta:
        model = Transaction
        fields = ("montant", "compte", "categorie", "date_transaction", "type_transaction")

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ("nom_categorie", "limite", "description_categorie")




