function navChange(btn) {
    $("li").removeClass("active");
    $(btn).addClass("active");
}

function searchDump(inputId){
    let searchInputValue = $("#" + inputId).val().split("-");
    let winLocation = window.location;
    let queryValue = "?st=" + searchInputValue[0] + "&sst=" + searchInputValue[1];
    if(String(winLocation).includes("dump"))
    {
        window.location = queryValue;
        return;
    }
    window.location = "dump" + queryValue; 
}
