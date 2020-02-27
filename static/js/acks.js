let _param_order = ["TimeSent", "Sat Time", "GroundTime", "Id", "CommandName", "AckType", "ErrorType"]

let acksList = $("#acks-list").data("acks");
acksList = JSON.parse(acksList.replace(/'/g, '"'));
acksList = acksList.Content;

let table = document.createElement("table");
table.className = "highlight white black-text";

let head = generateTableHead(table, _param_order);
let logsExportBtn = exportBtnGenerator();

$(logsExportBtn).click(function () {
    let filename = "AcksTable-" + getCurrentDate() + ".csv"
    exportTableToCSV(filename);
})

$("#table-container").addClass("scrollable-div");
$("#table-container").append(generateAllTable(head, acksList));
$("#btn-div").append(logsExportBtn);


let interval = setInterval(function () {
    $.ajax({
        type: "POST",
        url: `/acks`,
        data: {}
    }).done(function (params) {
        acksList = params.Content;

        refresh_table(acksList, "table-container", "white");
    });
}, 1000);