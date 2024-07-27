
export function delete_compte(delComt, suppComp, head, top_first, add_acc, all_page) {
    if (!null) {
        const deleteCompteSection = document.querySelector(delComt);
        const btn_delete = document.querySelectorAll(suppComp);
        const header_del = document.querySelector(head);
        const header_top = document.querySelector(top_first);
        const btn_add_compte = document.querySelector(add_acc);
        const body = document.querySelector(all_page);

        if (
            deleteCompteSection !== null &&
            btn_delete !== null &&
            header_del !== null &&
            header_top !== null &&
            btn_add_compte !== null &&
            body !== null
            ) 
            {

        deleteCompteSection.style.transform = "scale(0)";

        btn_delete.forEach(elm => {
            console.log(elm);
            elm.addEventListener("click", function() {
            
                deleteCompteSection.style.transform = "scale(100%)";
            })
        })

        let link = "http://127.0.0.1:8000/transaction/supprimerCompte/" + id_del;

        if (window.location.href === link) {
            deleteCompteSection.style.transform = "scale(100%)";
            header_del.style.filter = "blur(3px)";
            header_top.style.filter = "blur(3px)";
            btn_add_compte.style.filter = "blur(3px)";
            btn_add_compte.style.height = "100vh";
            body.style.overflowY = "hidden";
        } else {
            deleteCompteSection.style.transform = "scale(0)";
        }
    }

}

}

export function add_compte(addComt, btn_add, head, suppComp, header_as, topFirst, all_page) {
    if (!null) {
        const section_add_compte = document.querySelector(addComt);
        const btn_ajout = document.querySelector(btn_add);

        const btn_delete = document.querySelectorAll(head);
        const header_del = document.querySelector(suppComp);
        const header_top = document.querySelector(header_as);
        const btn_add_compte = document.querySelector(topFirst);
        const body = document.querySelector(all_page);

        if (
            section_add_compte !== null &&
            btn_ajout !== null &&
            btn_delete !== null &&
            header_del !== null &&
            btn_add_compte !== null &&
            body !== null
            ) 

            {

                section_add_compte.style.transform = "scale(0)";

                btn_ajout.addEventListener("click", function(e) {
                    section_add_compte.style.transform = "scale(100%)";
                    header_del.style.filter = "blur(3px)";
                    header_top.style.filter = "blur(3px)";
                    btn_add_compte.style.filter = "blur(3px)";
                    btn_add_compte.style.height = "100vh";
                    body.style.overflowY = "hidden";
                })
            }
    }

}




