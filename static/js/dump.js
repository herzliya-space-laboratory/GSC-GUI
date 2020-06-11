function createCharts() {
    let row = document.createElement("div");
    row.className = "row";
    let card = createCard(row);

    let options = $("meta[name=jinOptions]").attr("content");
    let data = $("meta[name=jinData]").attr("content");
    let units = $("meta[name=jinUnits]").attr("content");
    let telemType = $("meta[name=jinTelemType]").attr("content");
    let telemName = $("meta[name=jinTelemName]").attr("content");

    let title = document.createElement("title");
    title.innerHTML = telemName;
    document.head.appendChild(title);
    document.getElementById("title").innerHTML = telemName;

    data = JSON.parse(data.replace(/'/g, '"'));
    units = JSON.parse(units.replace(/'/g, '"'));
    options = JSON.parse(options.replace(/'/g, '"'));
    telemType = JSON.parse(telemType.replace(/'/g, '"'));


    let charts = initCardElements(card, data);
    document.getElementById("main").insertBefore(row,
        document.getElementById("main").firstChild);

    drawCharts(charts, options, data, units);

    setInterval(function () {
        updateCharts(charts, options, units, telemType);
    }, 1000);

    $("#exportCsv").click(function () {
        const num = document.getElementById("numCsv").value;
        getLatestPackets(num, telemType, telemName);
    })
}

function initCardElements(card, data) {
    let charts = {};
    for (let param in data) {
        let textbox = document.createElement("h6");
        card.appendChild(textbox);
        charts[param] = textbox;
    }

    return charts;
}

function createCard(div) {
    let col = document.createElement("div");
    col.className = "col s7";

    let card = document.createElement("div");
    card.className = "card white";

    let content = document.createElement("div");
    content.className = "card-content black-text";

    col.appendChild(card);
    card.appendChild(content);
    div.appendChild(col);

    return content;
}


function drawCharts(charts, options, data, units) {
    for (let i in data) {
        charts[i].innerHTML = `${i + " [" + units[i] + "]"}: ${data[i]}`;

        if (!options[i]) {
            charts[i].className = "black-text";
        }
        else if (data[i] > options[i]["rangeEnd"] || data[i] < options[i]["rangeStart"]) {
            charts[i].className = "red-text";
        } else {
            charts[i].className = "green-text";
        }
    }
}

function updateCharts(charts, options, units, telemType) {
    $.ajax({
        type: "POST",
        url: "/dump?st=" + telemType["st"] + "&sst=" + telemType["sst"],
        data: {}
    }).done(function (params) {
        drawCharts(charts, options, params, units);
    });
}

function getLatestPackets(num, telemType, telemName) {
    $.ajax({
        type: "POST",
        url: "/getLatestPackets?st=" + telemType["st"] + "&sst=" + telemType["sst"] + "&num=" + num,
        data: {}
    }).done(function (params) {
        exportObjArrToCSV(telemName, params.data);
    });
}

window.onload = createCharts();
