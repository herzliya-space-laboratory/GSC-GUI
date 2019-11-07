google.charts.load("current", { packages: ["gauge"] });
google.charts.setOnLoadCallback(createCharts);

function createCharts() {
    let dispType = {
        "3v3_curr": "gauge",
        batt_curr: "textbox",
        vbatt: "textbox"
    };
    const options = {
        "3v3_curr": {
            min: 1,
            max: 10,
            redFrom: 8
        },
        "batt_curr": {
            redFrom: 130
        },
        "vbatt": {
            redFrom: 80
        }
    };
    //$("meta[name=jinOptionsn]").attr("content");
    let data = $("meta[name=jinBeacon]").attr("content");
    let units = $("meta[name=jinUnits]").attr("content");

    data = JSON.parse(data.replace(/'/g, '"'));
    units = JSON.parse(units.replace(/'/g, '"'));
    //options = JSON.parse(units.replace(/'/g, '"'));

    let charts = {};
    let greatDiv = document.createElement("div");

    for (let i in data) {
        if (dispType[i] === "gauge") {
            let gauge = document.createElement("div");
            greatDiv.appendChild(gauge);
            $(gauge).css("display", "inline-block");
            charts[i] = new google.visualization.Gauge(gauge);
        } else if (dispType[i] === "textbox") {
            let textbox = document.createElement("textbox");
            greatDiv.appendChild(textbox);
            $(textbox).css("display", "inline-block");
            charts[i] = textbox;
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
        } else if (dispType[i] === "textbox") {
            charts[i].innerHTML = `${i + "[" + units[i] + "]"}: ${data[i]}`;
            $(charts[i]).css("font-size", "35px");
            if (
                data[i] >= options[i]["redFrom"]
            ) {
                $(charts[i]).css("color", "red");
                $(charts[i]).css("font-weight", "Bold");
                $(charts[i]).css("padding-left", "30px");
            } else {
                $(charts[i]).css("color", "black");
                $(charts[i]).css("font-weight", "Normal");
                $(charts[i]).css("padding-left", "30px");
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

