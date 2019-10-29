function dateParser(date_str) {
    date_str = date_str.split(" ");
    date = date_str[0].split("/");
    base_str_date = date[2] + "-" + date[1] + "-" + date[0];
    base_hour_str = "T" + date_str[1];
    return new Date(base_str_date + base_hour_str);
}

function sortByNewestTime(param_Dict) {
    let sat_time = param_Dict["Packet Sat Date Time"];

    sat_time.forEach(time => {
        time[1] = dateParser(time[1]);
    });

    return sat_time.sort((a, b) => b[1] - a[1]);
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
    let head_exp = param_order
    head_exp.forEach(key => {
        let thead_cell = createHeadCell(row, key)
        $(thead_cell).attr("scope", "col")
    });
    return table
}

function generateAllTable(table, data) {
    let time_sorted_data = $.extend(true, [], sortByNewestTime(data));
    let tbody = table.appendChild(document.createElement("tbody"));
    time_sorted_data.forEach(telem_param => {
        let row = tbody.insertRow();
        let headCell = createHeadCell(row, telem_param[1]);
        $(headCell).attr("scope", "row");
    });
    return table
}

function sortByNewestTime(param_Dict) {

    param_Dict.forEach(row => {
        row["Sat Time"] = dateParser(row["Sat Time"]);
    });

    return param_Dict.sort((a, b) => b["Sat Time"] - a["Sat Time"]);
}