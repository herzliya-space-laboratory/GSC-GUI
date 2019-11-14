let _param_order = ["Sat Time", "Ground Time", "Data", "Log Type", "System"];

let logsDict = $("#logs-dict").data("logs");
logsDict = JSON.parse(logsDict.replace(/'/g, '"'));

let table_div = document.createElement("div");
table_div.id = "table-div";
$(table_div).addClass("scrollable-div");

let table = document.createElement("table")
$(table).addClass("table").addClass("table-hover").addClass("table-dark");

let head = generateTableHead(table, logsDict, _param_order);

table_div.appendChild(generateAllTable(head, logsDict));

let exportBtn = document.createElement("button");
exportBtn.innerText = "Export table to csv file";
$(exportBtn).addClass("btn").addClass("btn-outline-primary");

$(exportBtn).click(function(){
    let filename = "LogsTable-" + getCurrentDate() + ".csv"
    exportTableToCSV(filename);
}) 

document.body.appendChild(table_div);
document.body.appendChild(exportBtn);

let interval = setInterval(function () {
    $.ajax({
        type: "POST",
        url: "/logs",
        data: {}
    }).done(function (params) {
        logsDict = JSON.parse(params.replace(/'/g, '"'));
        refresh_table(logsDict, _param_order, "table-div");
    });
}, 1000);

