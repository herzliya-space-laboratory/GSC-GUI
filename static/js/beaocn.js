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

    let charts = initCardElements(dispOrder, categoryCards);

    $("#main").append(row);

    drawCharts(charts, options, data, units, paramNames);

    setInterval(function () {
        updateCharts(charts, options, units, paramNames);
    }, 1000);
}

function initCardElements(dispOrder, cards) {
    let charts = {};
    for (let category in dispOrder) {
        let heading = document.createElement("span");
        heading.className = "card-title";
        heading.innerHTML = category;
        cards[category].appendChild(heading);
        for (let i in dispOrder[category]) {
            let param = dispOrder[category][i]
            let textbox = document.createElement("h6");
            cards[category].appendChild(textbox);
            charts[param] = textbox;
        }
    }

    return charts;
}

function createCards(dispOrder, div) {
    let cards = {};

    for (let i in dispOrder) {
        let col = document.createElement("div");
        col.className = "col l4 m6 s12";

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


function drawCharts(charts, options, data, units, paramNames) {
    for (let i in data) {
        paramName = paramNames[i] != null ? paramNames[i] : i;
        charts[i].innerHTML = `${paramName + " [" + units[i] + "]"}: ${data[i]}`;
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

function updateCharts(charts, options, dispType, units, paramNames) {
    $.ajax({
        type: "POST",
        url: "/beacon",
        data: {}
    }).done(function (params) {
        drawCharts(charts, options, params, dispType, units, paramNames);
    });
}

createCharts();
