import datetime
from django.shortcuts import get_object_or_404, redirect, render
import os
from django.contrib.auth import get_user_model
import pandas as pd 
import pytesseract
from PIL import Image
import uuid
from django.core.files import File as DjangoFile
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import AddCompteForm, CategorieForm, FileForm, TransactionForm
from .models import Transaction, Compte, File, Categorie, Alert


from emailSend.utils import SendMessageEmail
from django.utils.timezone import now


from .task import add

User = get_user_model()

@login_required
def import_relev_excel(request):
    form = FileForm(request.POST, request.FILES, user=request.user)
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            fichier = form.save(commit=False)
            compte_id = request.POST.get('compte')
            compte = Compte.objects.get(id=compte_id)  # Récupérer l'objet Compte correspondant
            fichier.compte = compte  # Associer le fichier au compte
            fichier.save()
            if str(fichier.file).endswith('.xlsx'):
                releve_df = pd.read_excel(fichier.file.path)
            elif str(fichier.file).endswith('.csv'):
                releve_df = pd.read_csv(fichier.file.path)
            elif str(fichier.file).endswith(('.png', '.jpg', '.jpeg')):
                img = Image.open(fichier.file.path)
                text = pytesseract.image_to_string(img)
                lignes = text.strip().split("\n")
                donnees = [ligne.split() for ligne in lignes if ligne]
                max_cols = max(len(ligne) for ligne in donnees)
                donnees = [ligne + [''] * (max_cols - len(ligne)) for ligne in donnees]
                df = pd.DataFrame(donnees[1:], columns=donnees[0])
                df.columns = df.columns.str.replace('_', ' ')
                nom_fichier_unique = "donnees_{}.xlsx".format(uuid.uuid4())
                chemin_fichier = os.path.join(os.path.dirname(fichier.file.path), nom_fichier_unique)
                df.to_excel(chemin_fichier, index=False)
                with open(chemin_fichier, 'rb') as f:
                    fichier_excel = File(file=DjangoFile(f, name=nom_fichier_unique))
                    fichier_excel.save()
                releve_df = df
            else:
                raise ValueError("Format de fichier non pris en charge")
            releve_df['Date'] = pd.to_datetime(releve_df['Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
            date_col = 'Date'
            montant_col = 'Montant'
            categorie_col = 'Categorie'
            type_transaction_col = 'Type transaction'
            for index, row in releve_df.iterrows():

                date_transaction = row[date_col]
                montant_transaction = row[montant_col]
                categorie_transaction = row[categorie_col]
                type_transaction_transaction = row[type_transaction_col]
                utilisateur = User.objects.get(id=request.user.id)
                user = request.user

                if Categorie.objects.filter(nom_categorie=categorie_transaction).exists():
                    categorie = Categorie.objects.filter(nom_categorie=categorie_transaction).first()
                else:
                    categorie = Categorie(nom_categorie=categorie_transaction, user=request.user)
                    categorie.save()

                transaction = Transaction(
                    montant=montant_transaction,
                    type_transaction=type_transaction_transaction,
                    date_transaction=date_transaction,
                    compte=compte,
                    categorie=categorie,
                    utilisateur=utilisateur,
                )
                transaction.save()
            return redirect("transaction:listeTransaction")
    else:
        form = FileForm(user=request.user)
    return render(request, "trans/file.html", {"form": form})




@login_required
def listeTransaction(request):
    user = request.user
    transation = Transaction.objects.filter(utilisateur=user).order_by("-date_transaction")[:10]

    all_categ = Categorie.objects.filter(user = user).order_by("-created_at")[:6]

    return render(request, "trans/lite_trans.html", {
        "transation_listes": transation,
        "all_categs": all_categ,
        })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import for decorator

@login_required
def addTransaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.utilisateur = request.user
            transaction.save()

            # Calcul du dépassement (en supposant que "montant" est un champ pour le montant de la transaction)

            # Calcul du total des transactions pour la catégorie dans le mois
            total_montant_categorie = Transaction.objects.filter(
            categorie=transaction.categorie,
            date_transaction__month=datetime.date.today().month,
            date_transaction__year=datetime.date.today().year,
            utilisateur=request.user
            ).aggregate(total=Sum('montant'))['total'] or 0
            calcDepassement = total_montant_categorie - transaction.categorie.limite

            if transaction.type_transaction == "Crédit" and total_montant_categorie > transaction.categorie.limite:
                # Logique de notification par e-mail
                try:
                    subject = "Alert de dépassement budgétaire"
                    template = "email/alertEmail.html"
                    context = {
                        "date": datetime.datetime.now(), 
                        "email": request.user.email,
                        "msg": f"Dépassement du montant dans la catégorie {transaction.categorie.nom_categorie} de {calcDepassement} $"
                    }
                    
                    email_sent = SendMessageEmail(subject=subject, receivers=[request.user.email], template=template, context=context)
                    if not email_sent:
                        print(f"Erreur lors de l'envoi de l'e-mail à {request.user.email}")
                except Exception as e:
                    print("Une erreur s'est produite lors de l'envoi de la notification par e-mail : {e}")

            elif transaction.type_transaction == "Débit" and total_montant_categorie < transaction.categorie.limite:
                # Logique de notification par e-mail
                try:
                    subject = "Alert de dépassement budgétaire"
                    template = "email/alertEmail.html"
                    context = context = {
                        "date": datetime.datetime.now(), 
                        "email": request.user.username,
                        "msg": f"insuffisance du montant dans la catégorie {transaction.categorie.nom_categorie} de {calcDepassement} $"
                    }
                    
                    email_sent = SendMessageEmail(subject=subject, receivers=[request.user.email], template=template, context=context)
                    if not email_sent:
                        print(f"Erreur lors de l'envoi de l'e-mail à {request.user.email}")
                except Exception as e:
                    print(f"Une erreur s'est produite lors de l'envoi de la notification par e-mail : {e}")
            
            return redirect("transaction:listeTransaction")
    else:
        form = TransactionForm(user=request.user)

    return render(request, "trans/ajouter_trans.html", {"transaction_form": form})


@login_required
def deleteTransaction(request, id):
    obj = get_object_or_404(Transaction, id=id)
    name_obj = obj.categorie.nom_categorie
    if request.method == "POST":
        obj.delete()
        return redirect("transaction:listeTransaction")
    return render(request, "trans/delete_trans.html", {
        "del_transaction_name": name_obj,
        })

login_required
def updateTransactiom(request, id):
    item = get_object_or_404(Transaction, id=id)
    form = TransactionForm(request.POST or None, instance=item)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=item)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.utilisateur = request.user
            new_object.save()
            return redirect("transaction:listeTransaction")
        else:
            form = TransactionForm(request.POST)

    return render(request, "trans/update_trans.html", {"form": form})


# fonctions de gestion des catégories

@login_required
def addCategorie(request):
    user = request.user
    categorie = Categorie.objects.filter(user=user)

    form = CategorieForm()
    if request.method == "POST":
        form = CategorieForm(request.POST)
        if form.is_valid():
            ajout_categorie = form.save(commit=False)
            ajout_categorie.user = user
            ajout_categorie.save()
            return redirect("transaction:listeTransaction")
        else:
            form = CategorieForm()
    return render(request, "trans/lite_trans.html", {"form": form,})


# vues de gestion des comptes

@login_required
def gestionCompte(request):
    user = request.user
    comptes = Compte.objects.filter(proprietaire=user)

    form = AddCompteForm()
    if request.method == "POST":
        form = AddCompteForm(data=request.POST)
        if form.is_valid():
            ajout_compte = form.save(commit=False)
            ajout_compte.proprietaire = request.user
            ajout_compte.save()
            return redirect("transaction:comptes")
        else:
            form = AddCompteForm()
    return render(request, "comptes/comptes.html", {
        "comptes": comptes,
        "form": form,
        })

@login_required
def supprimerCompte(request, id):
    obj = get_object_or_404(Compte, id=id)
    name_obj = obj.nom_compte or obj.operateur
    if request.method == "POST":
        obj.delete()
        return redirect("transaction:comptes")
    return render(request, "comptes/comptes.html", {"name_obj": name_obj, "id_del" : id})




def test_task(request):
    result = add.delay(2, 5)
    return render(request, "trans/test_task.html", {'result': result})

def test_task_result(request, task_id):
    result = add.AsyncResult(task_id)
    if result.ready():
        return render(request, "trans/test_task.html", {'result': result.result})
    return render(request, "trans/test_task_result.html", {'result': "result is not ready yet"})


def alertDepensement(request):
    all_alert = Alert.objects.filter(user=request.user)
    countAlert = all_alert.count()
    return render(request, "notification/alert.html", {"alert": all_alert, "countAlert": countAlert})