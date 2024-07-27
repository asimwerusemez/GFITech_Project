from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-cat1', 'placeholder': "Nom Complet"}), label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-cat1', 'placeholder': "Email"}), label='')
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-cat1', 'placeholder': "Télephone"}), label='')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Votre message..."}), label='')

    class Meta:
        model = Contact
        fields = (
            "nom", 
            "email", 
            "phone", 
            "message", 
        )