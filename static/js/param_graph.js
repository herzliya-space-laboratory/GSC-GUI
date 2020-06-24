let paramValues = $("#paramData").data("values");
let paramOptions = $("#paramOptions").data("values");
let paramName = JSON.parse($("#paramName").data("values").replace(/'/g, '"'));
let paramUnit = $("#paramUnit").data("values");
let isLineGraph = $("#isLineGraph").data("values");

if (paramOptions == undefined || paramOptions == "") {
	paramOptions = '{"rangeStart": "", "rangeEnd": ""}';
}

paramValues = JSON.parse(paramValues.replace(/'/g, '"'));
paramOptions = JSON.parse(paramOptions.replace(/'/g, '"'));

let title = document.createElement("title");
title.innerHTML = paramName[0];

rangesValidateBool =
	paramOptions["rangeStart"] == "" && paramOptions["rangeEnd"] == "";

if (rangesValidateBool) {
	paramOptions["rangeStart"] = null;
	paramOptions["rangeEnd"] = null;
}
let allParamValues = combineParamDicts(paramValues);
let paramArray = Object.keys(allParamValues).map(function (key) {
	// return [key, paramValues[key]];
	return [key, ...allParamValues[key]];
});

function combineParamDicts(paramArr) {
	let combined = {};
	for (let i = 0; i < paramArr.length; i++) {
		const param = paramArr[i];
		for (const key of Object.keys(param)) {
			if (!combined[key]) {
				combined[key] = [];
				for (let j = 0; j < paramArr.length; j++) {
					combined[key].push(undefined);
				}
			}
			if (!isNaN(param[key])) combined[key][i] = +param[key];
			else combined[key][i] = param[key];
		}
	}
	return combined;
}

let sortedArr = sortByNewestTime(paramArray);
sortedArr = addRagensToArray(paramOptions, sortedArr);

// google.charts.load('current', {packages: ['corechart']});
google.charts.load("current", { packages: ["line", "corechart"] });
google.charts.setOnLoadCallback(drawGraph);

function drawGraph() {
	var data = new google.visualization.DataTable();
	data.addColumn("datetime", "Time of dump");
	for (const param of paramName) {
		data.addColumn("number", `${param} [${paramUnit}]`);
	}
	data.addColumn("number", "rangeStart");
	data.addColumn("number", "rangeEnd");

	data.addRows(sortedArr);

	var options = {
		width: 1600,
		height: 500,
		hAxis: {
			title: "Time",
		},
		theme: "material",
		curveType: "function",
		vAxis: {
			title: `${paramName[0]} [${paramUnit}]`,
		},
		explorer: {
			actions: ["dragToZoom", "rightClickToReset"],
			axis: "vertical",
			keepInBounds: true,
			maxZoomIn: 1000000.0,
		},
	};

	var container = document.getElementById("chart_div");
	let materialChart;
	if (isLineGraph)
		materialChart = new google.visualization.LineChart(
			document.getElementById("chart_div")
		);
	else
		materialChart = new google.visualization.ScatterChart(
			document.getElementById("chart_div")
		);
	google.visualization.events.addListener(
		materialChart,
		"ready",
		function () {
			var labels = container.getElementsByTagName("text");
			Array.prototype.forEach.call(labels, function (label) {
				if (label.getAttribute("text-anchor") === "middle") {
					label.setAttribute(
						"y",
						parseFloat(label.getAttribute("y")) + 20
					);
				}
			});
		}
	);
	materialChart.draw(data, options);
}

function dateParser(date_str) {
	date_str = date_str.split(" ");
	date = date_str[0].split("/");
	base_str_date = date[2] + "-" + date[1] + "-" + date[0];
	timestr = date_str[1].split(":");
	timestr[0].padStart(2, "0");
	base_hour_str = "T" + timestr.join(":");
	return new Date(base_str_date + base_hour_str);
}

function sortByNewestTime(param_Dict) {
	param_Dict.forEach((time) => {
		time[0] = dateParser(time[0]);
		time[1] = Number(time[1]);
	});

	return param_Dict.sort((a, b) => a[0] - b[0]);
}

function addRagensToArray(options, arr) {
	arr.forEach((paramVal) => {
		paramVal.push(options["rangeStart"]);
		paramVal.push(options["rangeEnd"]);
	});
	return arr;
}
