if (document.getElementsByClassName("alert-fail")[0]) {
    flash = setInterval(() => {
        document.getElementsByClassName("alert-fail")[0].remove();
        clearInterval(flash);
    }, 2000);
}

if (document.getElementsByClassName("alert-success")[0]) {
    flash = setInterval(() => {
        document.getElementsByClassName("alert-success")[0].remove();
        clearInterval(flash);
    }, 2000);
}