let paramSelectOptions = [];

function searchDumpGraph(inputId, paramInputId) {
    let searchInputValue = $("#" + inputId).val();
    let param = $("#" + paramInputId).val();
    console.log(param);
    if (dumpDict[searchInputValue] == undefined) {

        alert(`Dump \"${searchInputValue}\" not found`)
        return;
    }
    let st = dumpDict[searchInputValue]["st"];
    let sst = dumpDict[searchInputValue]["sst"];
    let queryValue = "?st=" + st + "&sst=" + sst + "&paramName=" + param;
    console.log(queryValue);
    window.location = "paramGraph" + queryValue;
}

function createOptionsFromArr(arr) {
    for (let name of arr) {
        let option = document.createElement('option');
        option.value = name;
        option.innerHTML = name;
        document.getElementById('paramName').appendChild(option);
        paramSelectOptions.push(option);
    }
}

function removeElementsArr(arr) {
    while (arr.length > 0) {
        arr[0].remove();
        arr.shift();
    }
}

$(document).ready(function () {
    $('#telemName').autocomplete({
        data: createAutoCompleteDict(dumpDict)
    });

    document.getElementById('telemName').onchange = () => {
        let val = $('#telemName').val();
        if (val in dumpDict) {
            let st = dumpDict[val]["st"];
            let sst = dumpDict[val]["sst"];
            $.ajax({
                type: "GET",
                url: `/getTelemParams?st=${st}&sst=${sst}`,
                data: {}
            }).done(function (params) {
                createOptionsFromArr(params['params'])
            });
        }
        else {
            removeElementsArr(paramSelectOptions);
        }
    }
});


