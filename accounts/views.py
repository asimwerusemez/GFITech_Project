from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import ConnexionForm, CreateUserEntrepriseForm, CreateUserParticulierForm

def choice_profile(request):
    return render(request, "accounts/choice.html")

def register_entreprise(request):
    form = CreateUserEntrepriseForm()
    if request.method == "POST":
        form = CreateUserEntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:login')
        else:
            form = CreateUserEntrepriseForm()
    return render(request, "accounts/register.html", {"form":form})

def register_particulier(request):
    form = CreateUserParticulierForm()
    if request.method == "POST":
        form = CreateUserParticulierForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:login')
        else:
            form = CreateUserParticulierForm(request.POST, request.FILES)
    return render(request, "accounts/register.html", {"form":form})



def login_user(request):
    form = ConnexionForm(request.POST)
    if request.method == "POST":
        form = ConnexionForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:view_dash')
        else:
            form = ConnexionForm()
    return render(request, "accounts/login.html", {"form":form})

def logout_user(request):
    logout(request)
    return redirect('accounts:login')