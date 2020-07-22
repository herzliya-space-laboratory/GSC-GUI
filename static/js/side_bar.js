let dumpDict = {};

function navChange(btn) {
	$("li").removeClass("active");
	$(btn).addClass("active");
}

function searchDump(inputId) {
	let searchInputValue = $("#" + inputId).val();
	if (dumpDict[searchInputValue] == undefined) {
		alert(`Dump \"${searchInputValue}\" not found`);
		return;
	}
	let st = dumpDict[searchInputValue]["st"];
	let sst = dumpDict[searchInputValue]["sst"];
	let winLocation = window.location;
	let queryValue = "?st=" + st + "&sst=" + sst;
	if (String(winLocation).includes("dump")) {
		window.location = queryValue;
		return;
	}
	window.location = "dump" + queryValue;
}

function createAutoCompleteDict(dumpDict) {
	let autocompleteNames = {};
	for (let name in dumpDict) {
		autocompleteNames[name] = null;
	}

	return autocompleteNames;
}

function autoDumpSearch() {
	$.ajax({
		type: "GET",
		url: "/getDumpNames",
		data: {},
	}).done(function (params) {
		dumpDict = params;
		$(document).ready(function () {
			$("input.autocomplete" /*"#dump-search"*/).autocomplete({
				data: createAutoCompleteDict(params),
			});
		});
	});
}

document.onkeyup = function throwPrompt(e) {
	if (e.keyCode == 13) {
		searchDump("dump-seacrh");
	}
};

function fetchSatName() {
	fetch("./satName").then((res) => {
		res.text().then((satName) => {
			const namebox = document.getElementById("satName");
			namebox.innerHTML = `Satellite: ${satName}`;
		});
	});
}

window.onload = (() => {
	fetchSatName();
	autoDumpSearch();
})();
