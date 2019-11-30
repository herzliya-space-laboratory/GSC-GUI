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

    let charts = initCardElements(card, data);
    document.getElementById("main").appendChild(row);

    drawCharts(charts, options, data, units);

    setInterval(function () {
        updateCharts(charts, options, units, telemType);
    }, 1000);
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

        if ((options[i] != undefined || options[i] != null) && (data[i] > options[i]["rangeEnd"] || data[i] < options[i]["rangeStart"])) {
            charts[i].className = "red-text";
        } else {
            charts[i].className = "black-text";
        }
    }
}

function updateCharts(charts, options, units, telemType) {
    let data = {};
    $.ajax({
        type: "POST",
        url: "/dump/" + telemType,
        data: {}
    }).done(function (params) {
        data = params;
        drawCharts(charts, options, data, units);
    });
}

window.onload = createCharts();

