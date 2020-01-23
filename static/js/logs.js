let _param_order = ["Sat Time", "Ground Time", "Data", "Log Type", "System"];

$(document).ready(function(){
    $('select').formSelect();
  });

let logsDict = $("#logs-dict").data("logs");
logsDict = JSON.parse(logsDict.replace(/'/g, '"'));

$("#showCount").val(1);

let table = document.createElement("table");
table.className = "highlight white black-text";

let head = generateTableHead(table, _param_order);
let tableBody = document.createElement("table");
let logsExportBtn = exportBtnGenerator();

$(logsExportBtn).click(function () {
    let filename = "LogsTable-" + getCurrentDate() + ".csv"
    exportTableToCSV(filename);
})

$("#table-head-container").append(head);
$("#table-container").addClass("scrollable-div");
$("#table-container").append(generateAllTable(tableBody, logsDict));

$("#btn-div").append(logsExportBtn);

let interval = setInterval(function () {
    $.ajax({
        type: "POST",
        url: `/logs?sliceNum=${$("#showCount").val()}`,
        data: {}
    }).done(function (params) {
        logsDict = JSON.parse(params.replace(/'/g, '"'));

        refresh_table(logsDict, "table-container");
    });
}, 5000);

