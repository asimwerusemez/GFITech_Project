
export function ObjectifFinancier(addBtn, delBtn, updateBtn, addBtnAmount, addObject, delObject, dtDebut, dtFin) {
    // Boutons
    const btn_ajout = document.querySelector(addBtn);
    const btn_delete = document.querySelectorAll(delBtn);
    const btn_update_objectif = document.querySelectorAll(updateBtn);
    const btn_ajout_montant = document.querySelectorAll(addBtnAmount);

    // Divs
    const divAjoutObjectif = document.querySelector(addObject);
    const divSupprimerObjectif = document.querySelector(delObject);

    // Événements
    if (btn_ajout !== null) {
        btn_ajout.addEventListener("click", function(e) {
            divAjoutObjectif.style.display = "block";
            divSupprimerObjectif.style.display = "none";
        });
    }
    

    if (window.location.href == "http://127.0.0.1:8000/objectifs/ajouter") {
        divAjoutObjectif.style.display = "block";
        divSupprimerObjectif.style.display = "none";

        const header_del = document.querySelector(".header-aside");
        const header_top = document.querySelector(".top-first");

        const btn_ajout = document.querySelector(".add_objectif-btn");

        const body = document.querySelector("body");
        const all_objectif = document.querySelector(".all_progessions");

        header_del.style.filter = "blur(3px)";
        header_top.style.filter = "blur(3px)";
        btn_ajout.style.filter = "blur(3px)";
        all_objectif.style.filter = "blur(3px)";
        body.style.overflowY = "hidden";
    }

    btn_delete.forEach(element => {
        element.addEventListener("click", function(e) {
            divSupprimerObjectif.style.display = "block";
            divAjoutObjectif.style.display = "none";
        });
    });

    btn_update_objectif.forEach(element => {
        element.addEventListener("click", function(e) {
            divAjoutObjectif.style.display = "block";
            divSupprimerObjectif.style.display = "none";
        });
    });

    btn_ajout_montant.forEach(element => {
        element.addEventListener("click", function(e) {
            divAjoutObjectif.style.display = "block";
            divSupprimerObjectif.style.display = "none";
        });
    });

    let link_delete = "http://127.0.0.1:8000/objectifs/supprimer/" + id_delete;
    let link_update = "http://127.0.0.1:8000/objectifs/modifier/" + id_update_template;
    let link_ajout_montant = "http://127.0.0.1:8000/objectifs/ajout_montant_objectif/" + id_ajouter_montant;

    if (window.location.href == link_delete) {
        divSupprimerObjectif.style.display = "block";
        divAjoutObjectif.style.display = "none";

        const header_del = document.querySelector(".header-aside");
        const header_top = document.querySelector(".top-first");

        const btn_ajout = document.querySelector(".add_objectif-btn");

        const body = document.querySelector("body");
        const all_objectif = document.querySelector(".all_progessions");

        header_del.style.filter = "blur(3px)";
        header_top.style.filter = "blur(3px)";
        btn_ajout.style.filter = "blur(3px)";
        all_objectif.style.filter = "blur(3px)";
        body.style.overflowY = "hidden";
    }

    if (window.location.href == link_update) {
        divAjoutObjectif.style.display = "block";
        divSupprimerObjectif.style.display = "none";

        const header_del = document.querySelector(".header-aside");
        const header_top = document.querySelector(".top-first");

        const btn_ajout = document.querySelector(".add_objectif-btn");

        const body = document.querySelector("body");
        const all_objectif = document.querySelector(".all_progessions");

        header_del.style.filter = "blur(3px)";
        header_top.style.filter = "blur(3px)";
        btn_ajout.style.filter = "blur(3px)";
        all_objectif.style.filter = "blur(3px)";
        body.style.overflowY = "hidden";
    }

    if (window.location.href == link_ajout_montant) {
        divAjoutObjectif.style.display = "block";
        divSupprimerObjectif.style.display = "none";

        const header_del = document.querySelector(".header-aside");
        const header_top = document.querySelector(".top-first");

        const btn_ajout = document.querySelector(".add_objectif-btn");

        const body = document.querySelector("body");
        const all_objectif = document.querySelector(".all_progessions");

        header_del.style.filter = "blur(3px)";
        header_top.style.filter = "blur(3px)";
        btn_ajout.style.filter = "blur(3px)";
        all_objectif.style.filter = "blur(3px)";
        body.style.overflowY = "hidden";
    }

    // input

    const date_debut = document.getElementById(dtDebut);
    const date_fin = document.getElementById(dtFin);

    if (date_debut !== null || date_fin !== null) {
        date_debut.setAttribute("type", "date")
        date_fin.setAttribute("type", "date")
    }
    
}