function downloadCSV(csv, filename) {
    let csvFile;
    let downloadLink;

    csvFile = new Blob([csv], {type: "text/csv"});

    downloadLink = document.createElement("a");

    downloadLink.download = filename;

    downloadLink.href = window.URL.createObjectURL(csvFile);

    downloadLink.style.display = "none";

    document.body.appendChild(downloadLink);

    downloadLink.click();
}

function exportTableToCSV(filename) {
    let csv = [];
    let rows = document.querySelectorAll("table tr");
    
    for (let i = 0; i < rows.length; i++) {
        let row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (let j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
        csv.push(row.join(","));        
    }
    downloadCSV(csv.join("\n"), filename);
}

function getCurrentDate(){
    let currentDate = new Date();
    let year = currentDate.getFullYear().toString()
    let month = (currentDate.getMonth() + 1).toString()
    let day = currentDate.getDate().toString()
    let hour = currentDate.getHours().toString()
    let minute = currentDate.getMinutes().toString()
    let second = currentDate.getSeconds().toString()
    return day + "-" + month + "-" + year + "_" + hour + "-" + minute + "-" + second
}
