let _param_order = ["Sat Time", "Ground Time", "Data", "Log Type", "System"];

let logsDict = $("#logs-dict").data("logs");
logsDict = JSON.parse(logsDict.replace(/'/g, '"'));
logsDict = sortByNewestTime(logsDict);

let timesArray = getTimes(logsDict);

createOptionArr("firstDate", timesArray)
createOptionArr("secondDate", timesArray)

let table = document.createElement("table")
table.className = "highlight white black-text";

let head = generateTableHead(table, logsDict, _param_order);

let logsExportBtn = exportBtnGenerator();

$("#firstDate").val(logsDict[logsDict.length - 1]["Sat Time"])
$("#secondDate").val(logsDict[0]["Sat Time"])

let startRangeIndex = findDate($("#firstDate").val(), logsDict);
let endRangeIndex = findDate($("#secondDate").val(), logsDict);

$(logsExportBtn).click(function () {
    let filename = "LogsTable-" + getCurrentDate() + ".csv"
    exportTableToCSV(filename);
})

$("#table-container").addClass("scrollable-div");

$("#table-container").append(generateAllTable(head, logsDict, startRangeIndex, endRangeIndex));
$("#btn-div").append(logsExportBtn);

let interval = setInterval(function () {
    $.ajax({
        type: "POST",
        url: "/logs",
        data: {}
    }).done(function (params) {
        logsDict = JSON.parse(params.replace(/'/g, '"'));
        logsDict = sortByNewestTime(logsDict);

        startRangeIndex = findDate($("#firstDate").val(), logsDict);
        endRangeIndex = findDate($("#secondDate").val(), logsDict);

        $('#firstDate option[value="' + startRangeIndex + '"]').addClass("active")
        $('#secondDate option[value="' + endRangeIndex + '"]').addClass("active")

        refresh_table(logsDict, _param_order, "table-container", startRangeIndex, endRangeIndex);
    });
}, 1000);

