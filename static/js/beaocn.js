google.charts.load("current", { packages: ["gauge"] });
google.charts.setOnLoadCallback(createCharts);

function createCharts() {
    let options = $("meta[name=jinOptions]").attr("content");
    let data = $("meta[name=jinBeacon]").attr("content");
    let units = $("meta[name=jinUnits]").attr("content");
    let dispOrder = $("meta[name=jinDispOrder]").attr("content");
    let paramNames = $("meta[name=jinParamNames]").attr("content");

    data = JSON.parse(data.replace(/'/g, '"'));
    units = JSON.parse(units.replace(/'/g, '"'));
    options = JSON.parse(options.replace(/'/g, '"'));
    dispOrder = JSON.parse(dispOrder.replace(/'/g, '"'));
    paramNames = JSON.parse(paramNames.replace(/'/g, '"'));

    let row = document.createElement("div");
    row.className = "row";
    let categoryCards = createCards(dispOrder, row);

    let dispType = {};

    let charts = initCardElements(dispOrder, dispType, categoryCards);

    $("#main").append(row);

    drawCharts(charts, options, data, dispType, units, paramNames);

    setInterval(function () {
        updateCharts(charts, options, dispType, units, paramNames);
    }, 1000);
}

function initCardElements(dispOrder, dispType, cards) {
    let charts = {};
    for (let category in dispOrder) {
        let heading = document.createElement("span");
        heading.className = "card-title";
        heading.innerHTML = category;
        cards[category].appendChild(heading);
        for (let i in dispOrder[category]) {
            let param = dispOrder[category][i]
            if (dispType[param] === "gauge") {
                let gauge = document.createElement("div");
                cards[category].appendChild(gauge);
                charts[param] = new google.visualization.Gauge(gauge);
            } else /*if (dispType[param] === "textbox")*/ {
                let textbox = document.createElement("h6");
                cards[category].appendChild(textbox);
                charts[param] = textbox;
            }
        }
    }

    return charts;
}

function createCards(dispOrder, div) {
    let cards = {};

    for (let i in dispOrder) {
        let col = document.createElement("div");
        col.className = "col s4";

        let card = document.createElement("div");
        card.className = "card medium white";

        let content = document.createElement("div");
        content.className = "card-content black-text";

        col.appendChild(card);
        card.appendChild(content);
        cards[i] = content;

        div.appendChild(col);
    }

    return cards;
}


function drawCharts(charts, options, data, dispType, units, paramNames) {
    for (let i in data) {
        const option = options[i];
        paramName = paramNames[i] != null ? paramNames[i] : i;
        if (dispType[i] === "gauge") {
            const gaugeData = google.visualization.arrayToDataTable([
                ["Label", "Value"],
                [paramName + " [" + units[i] + "]", data[i]]
            ]);
            charts[i].draw(gaugeData, option);
        } else /*if (dispType[i] === "textbox")*/ {
            charts[i].innerHTML = `${paramName + " [" + units[i] + "]"}: ${data[i]}`;
            if ((options[i] != undefined || options[i] != null) && (data[i] > options[i]["rangeEnd"] || data[i] < options[i]["rangeStart"])) {
                charts[i].className = "black-text"//"red-text";
            } else {
                charts[i].className = "green-text";//"black-text";
            }
        }
    }
}

function updateCharts(charts, options, dispType, units, paramNames) {
    $.ajax({
        type: "POST",
        url: "/beacon",
        data: {}
    }).done(function (params) {
        drawCharts(charts, options, params, dispType, units, paramNames);
    });
}

