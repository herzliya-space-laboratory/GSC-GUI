google.charts.load("current", { packages: ["gauge"] });
google.charts.setOnLoadCallback(createCharts);

function createCharts() {
    let dispOrder = {
        "Info": ["sat_time"],
        "EPS": ["vbatt", "batt_curr", "3v3_curr", "5v_curr", "eps_temp[0]", "eps_temp[1]",
            "eps_temp[2]", "eps_temp[3]", "batt_temp[0]", "batt_temp[1]", "eps battery state"],
        "ADCS": ["altitudeangelsroll", "altitudeangelspich", "altitudeangelsyaw"],
        "TRXVU": ["lotrxvu_temp", "patrxvu_temp", "rxdoppler", "rxrssi", "txrefl", "txfrow"],
        "Payload": ["numberofpics"],
        "OBC": ["number_resets", "numberdelayd_comms", "last_resets", "states"]
    };

    let categoryCards = {};
    let greatDiv = document.createElement("div");
    greatDiv.className = "row";

    for (let i in dispOrder) {
        let col = document.createElement("div");
        col.className = "col s2";
        let card = document.createElement("div");
        card.className = "card white";
        let content = document.createElement("div");
        content.className = "card-content black-text";
        col.appendChild(card);
        card.appendChild(content);
        categoryCards[i] = content;
        greatDiv.appendChild(col);
    }

    let dispType = {
        "sat_time": "textbox",
        "3v3_curr": "textbox",
        "batt_curr": "textbox",
        "vbatt": "textbox"
    };

    let options = $("meta[name=jinOptions]").attr("content");
    let data = $("meta[name=jinBeacon]").attr("content");
    let units = $("meta[name=jinUnits]").attr("content");

    data = JSON.parse(data.replace(/'/g, '"'));
    units = JSON.parse(units.replace(/'/g, '"'));
    options = JSON.parse(options.replace(/'/g, '"'));

    let charts = {};


    for (let category in dispOrder) {
        let heading = document.createElement("span");
        heading.className = "card-title";
        heading.innerHTML = category;
        categoryCards[category].appendChild(heading);
        for (let i in dispOrder[category]) {
            let param = dispOrder[category][i]
            if (dispType[param] === "gauge") {
                let gauge = document.createElement("div");
                categoryCards[category].appendChild(gauge);
                charts[param] = new google.visualization.Gauge(gauge);
            } else /*if (dispType[param] === "textbox")*/ {
                let textbox = document.createElement("h6");
                categoryCards[category].appendChild(textbox);
                charts[param] = textbox;
            }
        }
    }
    document.body.appendChild(greatDiv);

    drawCharts(charts, options, data, dispType, units);

    setInterval(function () {
        updateCharts(charts, options, dispType, units);
    }, 1000);
}


function drawCharts(charts, options, data, dispType, units) {
    for (let i in data) {
        const option = options[i];
        if (dispType[i] === "gauge") {
            const gaugeData = google.visualization.arrayToDataTable([
                ["Label", "Value"],
                [i + "[" + units[i] + "]", data[i]]
            ]);
            charts[i].draw(gaugeData, option);
        } else /*if (dispType[i] === "textbox")*/ {
            charts[i].innerHTML = `${i + "[" + units[i] + "]"}: ${data[i]}`;
            //$(charts[i]).css("font-size", "25px");
            if (options[i] != undefined && (data[i] > options[i]["rangeEnd"] || data[i] < options[i]["rangeStart"])) {
                charts[i].className = "red-text";
            } else {
                charts[i].className = "black-text";
            }
        }
    }
}

function updateCharts(charts, options, dispType, units) {
    let beacon = {};
    $.ajax({
        type: "POST",
        url: "/beacon",
        data: {}
    }).done(function (params) {
        beacon = params;
        drawCharts(charts, options, beacon, dispType, units);
    });
}

