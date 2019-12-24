let paramValues = $("#paramData").data("values");
console.log(paramValues);
paramValues = JSON.parse(paramValues.replace(/'/g, '"'));

let paramArray = Object.keys(paramValues).map(function(key) {
    return [key, paramValues[key]];
  });

let sortedArr = sortByNewestTime(paramArray);

// google.charts.load('current', {packages: ['corechart']});
google.charts.load('current', {'packages':['line', 'corechart']});
google.charts.setOnLoadCallback(drawGraph);

function drawGraph(){
    var data = new google.visualization.DataTable();
    data.addColumn("datetime", "date of dump")
    data.addColumn("number", "param Values")

    data.addRows(sortedArr);

    var options = {
      width: 1600,
      height: 500,
      chartArea: {
        height: '100%',
        width: '100%',
        top: 24,
        left: 160,
        bottom: 100
      },
      hAxis: {
        title: 'Time'
      },
      vAxis: {
        title: 'Param Value'
      }
    };

    var container = document.getElementById('chart_div');
    var materialChart = new google.charts.Line(document.getElementById('chart_div'));
    google.visualization.events.addListener(materialChart, 'ready', function () {
      var labels = container.getElementsByTagName('text');
      Array.prototype.forEach.call(labels, function(label) {
        if (label.getAttribute('text-anchor') === 'middle') {
          label.setAttribute('y', parseFloat(label.getAttribute('y')) + 20);
        }
      });
    });
    materialChart.draw(data, options);
}

function dateParser(date_str) {
    date_str = date_str.split(" ");
    date = date_str[0].split("/");
    base_str_date = date[2] + "-" + date[1] + "-" + date[0];
    base_hour_str = "T" + date_str[1];
    return new Date(base_str_date + base_hour_str);
}

function sortByNewestTime(param_Dict) { 
  param_Dict.forEach(time => { 
      time[0] = dateParser(time[0]); 
      time[1] = Number(time[1])
  }); 

  return param_Dict.sort((a, b) => a[0] - b[0]); 
}
