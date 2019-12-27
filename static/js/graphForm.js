function searchDumpGraph(inputId, paramInputId) {
    let searchInputValue = $("#" + inputId).val();
    let param = $("#" + paramInputId).val();
    if (dumpDict[searchInputValue] == undefined) {

        alert(`Dump \"${searchInputValue}\" not found`)
        return;
    }
    let st = dumpDict[searchInputValue]["st"];
    let sst = dumpDict[searchInputValue]["sst"];
    let queryValue = "st=" + st + "&sst=" + sst + "&paramName=" + param;
    window.location.pathname = "paramGraph?" + queryValue;
}

$(document).ready(function () {
    $('#telemName').autocomplete({
        data: createDumpNameDict(dumpDict)
    });
});
