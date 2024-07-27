from django import forms

from transaction.models import Compte
from .models import ObjectifFinancier

class ObjectifFinancierForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['compte'].queryset = Compte.objects.filter(proprietaire=user)

    class Meta:
        model = ObjectifFinancier
        fields = ("motif", "cout", "montant_actuel", "compte", "date_debut", "date_fin")



class UpdateMontantForm(forms.ModelForm):
    class Meta:
        model = ObjectifFinancier
        fields = ['montant_actuel']

