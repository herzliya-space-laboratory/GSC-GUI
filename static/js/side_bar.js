function navChange(btn, element_id, mainId) {
    $(mainId).hide();
    $("#" + element_id).fadeIn();
    $(".side-nav-btn").removeClass("active");
    $(btn).addClass("active");
}

