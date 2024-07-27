import { delete_compte, add_compte } from "/static/js/modal_delete.js";
import { analyseRevenu } from "/static/js/analyse.js";
import { inp } from "/static/js/app.js";
import { ObjectifFinancier } from "/static/js/objectif.js";


if (window.location.href === "http://127.0.0.1:8000/transaction/ajout_categorie") {
        const target = document.querySelector(".Add-Categories");
        target.style.display = null;
        target.removeAttribute("aria-hidden");
        target.setAttribute("aria-modal", "true");
}


const closeModalCategorie = document.querySelector(".close-modal-categorie");
if (closeModalCategorie !== null) {
    closeModalCategorie.addEventListener("click", e => {
        const target = document.querySelector(".Add-Categories");
        target.style.display = "none";
        target.setAttribute("aria-hidden", "true");
        target.removeAttribute("aria-modal");
        window.location.href = "http://127.0.0.1:8000/transaction/";
    })
}


delete_compte(
    ".delete-compte", ".supprimer-compte", ".header-aside", ".top-first", ".add-compte", "body"
    );

add_compte(
    ".ajout_compte", ".btn-ajout", ".supprimer-compte", ".header-aside", ".top-first", ".add-compte", "body"
);

ObjectifFinancier(
    ".add_objectif-btn", ".btn-delete", ".btn-update", ".btn-add-montant", ".ajouter_objectif", ".supprimer-objectif", "id_date_debut", "id_date_fin"
    );

analyseRevenu('.tab-link')
inp("#id_date_transaction");


// const inputDate = document.querySelector("#id_date_transaction");
// inputDate.setAttribute("type", "date");