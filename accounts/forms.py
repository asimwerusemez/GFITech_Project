from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserEntrepriseForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}), label='')

    nom_entreprise = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'entreprise"}), label='')

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Entre votre Email"}), label='')

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Créer un Mot de passe"}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirmation mot de passe"}), label='')
    photo_profil = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': "Votre Photo de profile"}), label='Votre photo de profile')

    entrerprise = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = (
            "username", 
            "nom_entreprise",
            "email",
            "password1",  
            "password2",
            "photo_profil",
            "entrerprise",
        )


class CreateUserParticulierForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}), label='')
    profession = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Profession"}), label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Entre votre Email"}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Créer un Mot de passe"}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirmation mot de passe"}), label='')
    photo_profil = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': "Votre Photo de profile"}), label='Votre photo de profile')

    particulier = forms.BooleanField(initial=True, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = (
            "username", 
            "profession",
            "email",
            "password1",  
            "password2",
            "photo_profil",
            "particulier",
        )



class ConnexionForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'votre-classe-css', 
        'placeholder': "Nom d'utilisateur", 
    }), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'votre-classe-css',
        'placeholder': 'Mot de passe', 
    }), label='')

    class Meta:
        model = User
        fields = ('username', 'password')

