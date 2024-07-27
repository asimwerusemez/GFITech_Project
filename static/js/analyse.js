
export function analyseRevenu(tab) {
    let tabs = document.querySelectorAll(tab);

    if (tabs !== null) {
        tabs.forEach(tab => {
            tab.addEventListener("click", ()=> {
                unSelectAll();
                tab.classList.add('active');
                let ref = tab.getAttribute('data-ref');
                document.querySelector(`.tab-body[data-id="${ref}"]`).classList.add('active');
            });
        });
    
        function unSelectAll() {
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });
            let tabBodies = document.querySelectorAll('.tab-body');
            tabBodies.forEach(tab => {
                tab.classList.remove('active');
            })
        }
    }
}

