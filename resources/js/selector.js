export function changeMark(isButton, current) {
    const input = document.getElementById("input-mark");
    if (isButton) {
        processMarks((v) => v != current.textContent);
        input.value = current.textContent;
        input.textContent = current.textContent;
    } else {
        processMarks((v) => input.value && input.value != "" && v.indexOf(input.value) == -1);
    }
    input.textContent = input.value;
}

export function changeTaste(isButton, current) {
    const input = document.getElementById("input-taste");
    // const markName = current.name.split("-")[current.name.split("-").length - 1];
    if (isButton) {
        input.value = current.textContent;
        // processMarks((v) => v != markName);
    }
    input.textContent = input.value;
}

// включает разделы с маркой, которая needOff(markName) -> false
export function processMarks(needOff) {
    const marks = document.getElementsByName("mark-dropdown");
    for (let i = 0; i < marks.length; i++) {
        var className = marks[i].className;
        if (needOff(marks[i].textContent)) {
            className = className.replace("d-inline", "d-none");
            marks[i].className = className;

            processTastes(marks[i].textContent, "d-inline", "d-none");
        } else {
            className = className.replace("d-none", "d-inline");
            marks[i].className = className;

            processTastes(marks[i].textContent, "d-none", "d-inline");
        }
    }
}

export function processTastes(markName, from, to) {
    var tastes = document.getElementsByName("taste-dropdown-" + markName);
    var tasteSups = document.getElementsByName("taste-dropdown-sup-" + markName);
    var className;
    for (let i = 0; i < tastes.length; i++) {
        className = tastes[i].className;
        className = className.replace(from, to);
        tastes[i].className = className;
    }

    for (let i = 0; i < tasteSups.length; i++) {
        className = tasteSups[i].className;
        className = className.replace(from, to);
        tasteSups[i].className = className;
    }
}

export function changeStatButton(isTaste) {
    var primary, second;
    if (isTaste) {
        primary = document.getElementById("tabac");
        second = document.getElementById("recipe");
    } else {
        primary = document.getElementById("recipe");
        second = document.getElementById("tabac");
    }
    var className;
    className = primary.className.replace("btn-secondary", "btn-primary");
    primary.className = className;
    className = second.className.replace("btn-primary", "btn-secondary");
    second.className = className;
}