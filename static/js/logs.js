let _param_order = ["Sat Time", "Ground Time", "File Name", "Data", "Log Type", "System"];

let logsDict = $("#logs-dict").data("logs");
logsDict = JSON.parse(logsDict.replace(/'/g, '"'));

function dateParser(date_str) {
    date_str = date_str.split(" ");
    date = date_str[0].split("/");
    base_str_date = date[2] + "-" + date[1] + "-" + date[0];
    base_hour_str = "T" + date_str[1];
    return new Date(base_str_date + base_hour_str);
}

function createCell(row, text) {
    let cell = row.insertCell()
    let cell_text = document.createTextNode(text)
    cell.appendChild(cell_text)
}

function createHeadCell(row, text) {
    let head_cell = document.createElement("th");
    let head_cell_text = document.createTextNode(text);
    head_cell.appendChild(head_cell_text);
    row.appendChild(head_cell);
    return head_cell
}

function generateTableHead(table, param_Dict, param_order) {
    if (Object.keys(param_Dict) < 1) {
        return;
    }
    let thead = table.createTHead();
    let row = thead.insertRow();
    param_order.forEach(key => {
        let thead_cell = createHeadCell(row, key)
        $(thead_cell).attr("scope", "col")
    });
    return table
}

function genarateRowCelles(telem_param, row){
    createCell(row, telem_param[_param_order[1]]);
    createCell(row, telem_param[_param_order[2]]);
    createCell(row, telem_param[_param_order[3]]);
    createCell(row, telem_param[_param_order[4]]);
    createCell(row, telem_param[_param_order[5]]);
}

function generateAllTable(table, data) {
    let time_sorted_data = $.extend(true, [], sortByNewestTime(data));
    let tbody = table.appendChild(document.createElement("tbody"));
    time_sorted_data.forEach(telem_param => {
        let row = tbody.insertRow();
        $(row).addClass(telem_param["Color"])
        let headCell = createHeadCell(row, telem_param[_param_order[0]]);
        genarateRowCelles(telem_param, row);
        $(headCell).attr("scope", "row");
    });
    return table
}

function sortByNewestTime(param_Dict) {

    return param_Dict.sort((a, b) => dateParser(b["Sat Time"]) - dateParser(a["Sat Time"]));
}

function refresh_table(table_params) {
    let table_div = document.getElementById("table-div");
    table_div.innerHTML = "";

    let table = document.createElement("table");
    $(table).addClass("table").addClass("table-hover").addClass("table-dark");

    let head = generateTableHead(table, table_params, _param_order);

    table_div.appendChild(generateAllTable(head, table_params));
}

function getCurrentDate(){
    let currentDate = new Date();
    let year = currentDate.getFullYear().toString()
    let month = (currentDate.getMonth() + 1).toString()
    let day = currentDate.getDate().toString()
    let hour = currentDate.getHours().toString()
    let minute = currentDate.getMinutes().toString()
    let second = currentDate.getSeconds().toString()
    return day + "-" + month + "-" + year + "-" + hour + "-" + minute + "-" + second
}


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
        refresh_table(logsDict);
    });
}, 1000);

