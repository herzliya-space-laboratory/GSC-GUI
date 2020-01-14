let _param_order = ["Sat Time", "Ground Time", "Data", "Log Type", "System"];

$(document).ready(function(){
    $('select').formSelect();
  });

let logsDict = $("#logs-dict").data("logs");
logsDict = JSON.parse(logsDict.replace(/'/g, '"'));

$("#showCount").val(0);

let table = document.createElement("table")
table.className = "highlight white black-text";

let head = generateTableHead(table, logsDict, _param_order);

let logsExportBtn = exportBtnGenerator();

$(logsExportBtn).click(function () {
    let filename = "LogsTable-" + getCurrentDate() + ".csv"
    exportTableToCSV(filename);
})


$("#table-container").addClass("scrollable-div");
$("#table-container").append(generateAllTable(head, logsDict));

$("#btn-div").append(logsExportBtn);

let interval = setInterval(function () {
    $.ajax({
        type: "POST",
        url: `/logs?sliceNum=${$("#showCount").val()}`,
        data: {}
    }).done(function (params) {
        logsDict = JSON.parse(params.replace(/'/g, '"'));

        refresh_table(logsDict, _param_order, "table-container");
    });
}, 1000);

