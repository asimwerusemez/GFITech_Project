from django.shortcuts import render
from .models import Contact
from .forms import ContactForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "home/accueil.html")

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "home/confirmation.html")
        else:
            form = ContactForm()

    return render(request, "home/contact.html", {"form": form})

def fonctionnalite(request):
    return render(request, "home/fonctionnalite.html")



