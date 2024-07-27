from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ObjectifFinancierForm
from .models import ObjectifFinancier
from .forms import UpdateMontantForm



# la vue pour lister tout les objectifs
login_required
def objectif_view(request):
    objectif = []
    montant_actuel = []
    objectifs = ObjectifFinancier.objects.filter(utilisateur=request.user)

    # generer le graphique de progression
    progressions = ObjectifFinancier.objects.filter(utilisateur=request.user).order_by("cout")[:2]

    for progression in progressions:
        objectif.append(float(progression.objectif))
    for montant in progressions:
        montant_actuel.append(float(montant.montant_actuel))

    return render(request, "objectif/object_list.html", {
        "objectifs": objectifs, "progressions": progressions,
        "objectif": objectif,
        "montant_actuel": montant_actuel,
        })

# ajout objectif
login_required
def object_add(request):
    form = ObjectifFinancierForm(request.POST or None, user=request.user)

    if request.method == "POST":
        form = ObjectifFinancierForm(request.POST, user=request.user)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.utilisateur = request.user
            new_object.save()
            return redirect("objectif:objectif_view")
        else:
            form = ObjectifFinancierForm(request.POST)

    return render(request, "objectif/object_list.html", {"form": form})

# modification de l'objectif
login_required
def update_object(request, id):
    item = get_object_or_404(ObjectifFinancier, id=id)
    form = ObjectifFinancierForm(request.POST or None, instance=item)
    if request.method == "POST":
        form = ObjectifFinancierForm(request.POST, instance=item)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.utilisateur = request.user
            new_object.save()
            return redirect("objectif:objectif_view")
        else:
            form = ObjectifFinancierForm(request.POST)

    return render(request, "objectif/object_list.html", {"form": form, "id_update_objectif": id})

# supprimer un objectif

login_required
def delete_object(request, id):
    item = get_object_or_404(ObjectifFinancier, id=id)
    name_item = item.motif
    if request.method == "POST":
        item.delete()
        return redirect("objectif:objectif_view")
    return render(request, "objectif/object_list.html", {"name_item": name_item, "id_objectif_del": id})

@login_required
def ajout_montant_objectif(request, id):
    message = "vide"
    objectif = ObjectifFinancier.objects.get(id=id)
    form = UpdateMontantForm(request.POST, instance=objectif)
    if request.method == 'POST':
        form = UpdateMontantForm(request.POST, instance=objectif)
        if form.is_valid():
            form.save()
            message = messages.success(request, 'Le montant actuel a été mis à jour avec succès.')
            return redirect('objectif:objectif_view')
    else:
        form = UpdateMontantForm(instance=objectif)

    print(message)

    return render(request, "objectif/object_list.html", 
            {
            'form': form, 
            "message" : message,
            "id_ajouter_montant_objectif" : id,
        })

