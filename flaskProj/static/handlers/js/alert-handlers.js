export function alertHandler()
{
    if (document.getElementsByClassName("alert-fail")[0])
    {
        flash = setTimeout(() =>
        {
            document.getElementsByClassName("alert-fail")[0].remove();
        }, 2000);
    }

    if (document.getElementsByClassName("alert-success")[0])
    {
        flash = setTimeout(() =>
        {
            document.getElementsByClassName("alert-success")[0].remove();
        }, 2000);
    }
}