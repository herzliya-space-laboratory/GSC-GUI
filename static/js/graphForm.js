let paramSelectOptions = [];

function searchDumpGraph(inputId, paramInputId, isLineGraphId) {
    let isLineGraph = $("#" + isLineGraphId).prop("checked");
    let searchInputValue = $("#" + inputId).val();
    let param = $("#" + paramInputId).val();
    const startDate = decodeDateTime(document.getElementById("startDate").value);
    const endDate = decodeDateTime(document.getElementById("endDate").value);
    if (dumpDict[searchInputValue] == undefined) {

        alert(`Dump \"${searchInputValue}\" not found`)
        return;
    }
    let st = dumpDict[searchInputValue]["st"];
    let sst = dumpDict[searchInputValue]["sst"];
    let queryValue = `?st=${st}&sst=${sst}&paramName=${param}&isLineGraph=${isLineGraph}&startDate=${startDate}&endDate=${endDate}`;
    window.location = "paramGraph" + queryValue;
}

function decodeDateTime(dateTime) {
    //1970-01-02T01:01:01
    let parsed = dateTime.split("T");
    let time = parsed[1];
    let date = parsed[0].split("-");
    return `${date[2]}/${date[1]}/${date[0]} ${time}`;
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


