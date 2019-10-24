google.charts.load('current', { 'packages': ['gauge'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    let dispType = {};
    const options = getGaugesOptions(dispType);
    let gauges = new Array();
    let texts = new Array();
    let data = getLatestBeacon();

    for (let i = 0; i < options.length; i++) {
        if (dispType[data[i][0]] === "gauge") {
            let gauge = document.createElement("div");
            document.body.appendChild(gauge);
            gauges.push(new google.visualization.Gauge(gauge));
        }
        else if (dispType[data[i][0]] === "textbox") {
            let textbox = document.createElement("textbox");
            document.body.appendChild(textbox);
            texts.push(textbox);
        }

    }

    drawCharts(gauges, options, data, dispType);

    setInterval(function () {
        data = getLatestBeacon();
        drawCharts(gauges, options, data, dispType);
    }, 1000);
}

function drawCharts(charts, options, data, dispType) {
    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        if (dispType[data[i][0]] === "gauge") {
            const gaugeData = google.arrayToDataTable(data[i])
            charts[i].draw(gaugeData, option);
        }
        else if (dispType[data[i][0]] === "textbox") {
            const data = data[i][1];
            charts[i].innerHTML = data;
        }
    }
}

function getLatestBeacon() {
    let data;
    $.ajax({
        type: "POST",
        url: "/feed",
        data: {}
    }).done(function (params) {
        beacon = params;
    });

    let beacon = [];
    for (let index = 0; index < data.length; index++) {
        beacon.push(data[index]);
    }
    return beacon;
}

function getGaugesOptions(dispType) {
    let optionData = new Array();
    //DOTO: Implement getting options

    let options = new Array();

    for (let i = 0; i < optionsData.length; i++) {
        const optionData = optionsData[i];
        if (dispType[optionData[0]] === "gauge") {
            options.push({
                width: 400, height: 120,
                redFrom: optionData[1], redTo: optionData[2],
                minorTicks: 5
            });
        }
        else if (dispType[optionData[0]] === "textbox") {
            options.push(optionData[1]);
        }
    }

    return options;
}