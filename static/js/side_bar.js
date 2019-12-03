function navChange(btn) {
    $("li").removeClass("active");
    $(btn).addClass("active");
}

function searchDump(inputId){
    let searchInputValue = $("#" + inputId).val();
    let winLocation = window.location;
    if(String(winLocation).includes("dump"))
    {
        window.location = searchInputValue;
        return;
    }
    window.location = "dump/" + searchInputValue; 
}
