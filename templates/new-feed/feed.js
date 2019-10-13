google.charts.load('current', { 'packages': ['gauge'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    const options = getGaugesOptions();
    let gauges = new Array();
    let data = getLatestBeacon();

    for (let i = 0; i < options.length; i++) {
        let gauge = document.createElement(data[i][1] + "-gauge");

        document.body.appendChild(gauge);
        gauges.push(new google.visualization.Gauge(gauge));
    }

    drawGauges(gauges, options, data);

    setInterval(function () {
        data = getLatestBeacon();
        drawGauges(gauges, options, data);
    }, 1000);
}

function drawGauges(chart, options, data) {
    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        const gaugeData = google.arrayToDataTable(data[i])
        chart[i].draw(gaugeData, option);
    }
}

function getLatestBeacon() {

}

function getGaugesOptions() {
    let optionData = new Array();
    //DOTO: Implement getting options

    let options = new Array();

    for (let i = 0; i < optionsData.length; i++) {
        const optionData = optionsData[i];
        options.push({
            width: 400, height: 120,
            redFrom: optionData[0], redTo: optionData[1],
            minorTicks: 5
        });
    }

    return options;
}