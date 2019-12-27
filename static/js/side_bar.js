let dumpDict = {};

function navChange(btn) {
    $("li").removeClass("active");
    $(btn).addClass("active");
}

function searchDump(inputId) {
    let searchInputValue = $("#" + inputId).val();
    if (dumpDict[searchInputValue] == undefined) {

        alert(`Dump \"${searchInputValue}\" not found`)
        return;
    }
    let st = dumpDict[searchInputValue]["st"];
    let sst = dumpDict[searchInputValue]["sst"];
    let winLocation = window.location;
    let queryValue = "?st=" + st + "&sst=" + sst;
    if (String(winLocation).includes("dump")) {
        window.location = queryValue;
        return;
    }
    window.location = "dump" + queryValue;
}

function createDumpNameDict(dumpDict) {
    let dumpNames = {};
    for (let name in dumpDict) {
        dumpNames[name] = null;
    }

    return dumpNames;
}

function autoDumpSearch() {
    $.ajax({
        type: "GET",
        url: "/getDumpNames",
        data: {}
    }).done(function (params) {
        dumpDict = params;
        $(document).ready(function () {
            $("input.autocomplete"/*"#dump-search"*/).autocomplete({
                data: createDumpNameDict(params)
            });
        });
    });
}

document.onkeyup = function throwPrompt(e) {
    if (e.keyCode == 13) {
        searchDump("dump-seacrh")
    }
}

window.onload = autoDumpSearch();
