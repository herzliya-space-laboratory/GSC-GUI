let _param_order = ["Sat Time", "Ground Time", "Data", "Log Type", "System"];

let logsDict = $("#logs-dict").data("logs");
logsDict = JSON.parse(logsDict.replace(/'/g, '"'));

let table = document.createElement("table")
table.className = "highlight white black-text";

let head = generateTableHead(table, logsDict, _param_order);

let exportBtn = document.createElement("button");
exportBtn.innerText = "Export table to csv file";
exportBtn.className = "btn pink accent-3 white-text waves-effect"

$(exportBtn).click(function(){
    let filename = "LogsTable-" + getCurrentDate() + ".csv"
    exportTableToCSV(filename);
})

$("#table-container").addClass("scrollable-div");

$("#table-container").append(generateAllTable(head, logsDict));
$("#btn-div").append(exportBtn);

let interval = setInterval(function () {
    $.ajax({
        type: "POST",
        url: "/logs",
        data: {}
    }).done(function (params) {
        logsDict = JSON.parse(params.replace(/'/g, '"'));
        refresh_table(logsDict, _param_order, "table-container");
    });
}, 1000);

