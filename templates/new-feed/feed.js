google.charts.load('current', { 'packages': ['gauge'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    let dispType = {
        "hello": "gauge",
        "bla": "textbox",
        "blu": "gauge"
    };
    const options = [{
        width: 400, height: 120,
        redFrom: 80, redTo: 100,
        minorTicks: 5
    }, "5",
    {
        width: 400, height: 120,
        redFrom: 80, redTo: 100,
        minorTicks: 5
    }];//getGaugesOptions(dispType);
    let charts = new Array();
    let data = getLatestBeacon();
    let greatDiv = document.createElement("div");

    for (let i = 0; i < options.length; i++) {
        if (dispType[data[i][0]] === "gauge") {
            let gauge = document.createElement("div");
            greatDiv.appendChild(gauge);
            $(gauge).css('display', 'inline-block');
            charts.push(new google.visualization.Gauge(gauge));
        }
        else if (dispType[data[i][0]] === "textbox") {
            let textbox = document.createElement("textbox");
            greatDiv.appendChild(textbox);
            $(textbox).css('display', 'inline-block');
            charts.push(textbox);
        }

    }

    document.body.appendChild(greatDiv);

    drawCharts(charts, options, data, dispType);

    setInterval(function () {
        data = getLatestBeacon();
        drawCharts(charts, options, data, dispType);
    }, 1000);
}

function drawCharts(charts, options, data, dispType) {
    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        if (dispType[data[i][0]] === "gauge") {
            const gaugeData = google.visualization.arrayToDataTable([['Label', 'Value'], data[i]])
            charts[i].draw(gaugeData, option);
        }
        else if (dispType[data[i][0]] === "textbox") {
            const textboxData = data[i];
            charts[i].innerHTML = `${textboxData[0]}: ${textboxData[1]}`;
        }
    }
}

function getLatestBeacon() {
    /*let data;
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
    */
    return [["hello", 90], ["bla", 44], ["blu", 40]];
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