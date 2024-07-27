

export function inp(date) {
    const inputDate = document.querySelector(date);
    if (inputDate !== null) {
        inputDate.setAttribute("type", "date");
    }
}

