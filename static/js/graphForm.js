let paramNum = 1;

function searchGraph() {
    const isLineGraph = document.getElementById("isLineGraph").checked;
    const startDate = decodeDateTime(document.getElementById("startDate").value);
    const endDate = decodeDateTime(document.getElementById("endDate").value);
    const params = document.getElementById("params");
    const paramList = [];
    for (const param of params.children) {
        const telemName = param.getElementsByClassName("telemName")[0].value;
        if (dumpDict[telemName] == undefined) {
            alert(`Dump \"${searchInputValue}\" not found`)
            return;
        }
        const st = dumpDict[telemName]["st"];
        const sst = dumpDict[telemName]["sst"];
        const paramName = param.getElementsByClassName("paramName")[0].value;
        paramList.push({
            st,
            sst,
            paramName
        })
    }
    const query = `?params=${JSON.stringify(paramList)}&isLineGraph=${isLineGraph}&startDate=${startDate}&endDate=${endDate}`;
    window.location = "paramGraph" + query;
}

function decodeDateTime(dateTime) {
    //1970-01-02T01:01:01
    let parsed = dateTime.split("T");
    let time = parsed[1];
    let date = parsed[0].split("-");
    return `${date[2]}/${date[1]}/${date[0]} ${time}`;
}

function createOptionsFromArr(arr, paramIdx) {
    const paramsDiv = document.getElementById(`param${paramIdx}`);
    const selects = paramsDiv.querySelectorAll('select');
    for (let name of arr) {
        let option = document.createElement('option');
        option.value = name;
        option.innerHTML = name;
        for (const select of selects) {
            select.appendChild(option);
        }
    }
}

function removeParamSelectOptions(idx) {
    const select = document.getElementById(`param${idx}`).getElementsByClassName("paramName")[0];
    select.innerHTML = "";
}

function addParam() {
    const param = document.createElement("div");
    param.id = `param${paramNum}`;
    param.innerHTML = `<h6>Param ${paramNum + 1}:</h6>
                            <div class="input-field">
                                <label>Telemetry Name</label>
                                <input type="text" class="autocomplete telemName">
                            </div>
                            <div class="input-field">
                                <p>Parameter Name</p>
                                <select class="browser-default paramName">
                                </select>
                            </div>`
    document.getElementById("params").appendChild(param);
    $(param).find(".telemName").autocomplete({
        data: createAutoCompleteDict(dumpDict)
    })
    const index = paramNum;
    param.getElementsByClassName("telemName")[0].onchange = () => {
        let val = $(param).find(".telemName").val();
        if (val in dumpDict) {
            let st = dumpDict[val]["st"];
            let sst = dumpDict[val]["sst"];
            $.ajax({
                type: "GET",
                url: `/getTelemParams?st=${st}&sst=${sst}`,
                data: {}
            }).done(function (params) {
                createOptionsFromArr(params['params'], index)
            });
        }
        else {
            removeParamSelectOptions(index);
        }
    }
    paramNum++;
}

function deleteParam() {
    if (paramNum != 1) {
        document.getElementById("params").lastChild.remove();
        paramNum--;
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
                createOptionsFromArr(params['params'], 0)
            });
        }
        else {
            removeParamSelectOptions(0);
        }
    }
});


