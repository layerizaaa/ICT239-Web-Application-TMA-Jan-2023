var ctx = document.getElementById('swingChart').getContext('2d');

// Retrieve email id from element with id 'swingChart'
var email_id = $("#swingChart").attr("email_id")

$.ajax({
  url:"/swingchart",
  type:"POST",
  contentType: 'application/json;charset=UTF-8',
  data: JSON.stringify({'email_id': email_id}),
  error: function() {
      alert("Error");
  },
  success: function(data, status, xhr) {

    var chartDim = {};
      
    var chartDim = data.chartDim; 
    var xLabels = data.labels;

    // # New Output 
    // # var chartDim = data.chartDim; 
    // # {'usr_1': [[datetime1, 600], [datetime2, 600], ...], {'hotel_2': [[],[], ...]}  ...}
    // # var xLabels = data.labels;
    // # // [] 

    //debugger
    var vLabels = []; 
    // ['usr_1', 'usr_2', ...] 
    var vData = [];
    // [ [{'x': datetime_1, 'y':666}, {'x': datetime_2, 'y':1200} ...]

    for (const [key, values] of Object.entries(chartDim)) {
      vLabels.push(key);
      let xy = [];
      for (let i = 0; i < values.length; i++) {
        let d = new Date(values[i][0]);
        let year = d.getFullYear();
        let month = ('' + (d.getMonth() + 1)).padStart(2, '0');
        let day = ('' + d.getDate()).padStart(2, '0');
        let hour = ('' + d.getHours()).padStart(2, '0');
        let mins = ('' + d.getMinutes()).padStart(2, '0');
        aDateTime = year + '-' + month + '-' + day + ' ' + hour + ':' + mins;
        xy.push({ 'x': aDateTime, 'y': values[i][1] });
      }
      vData.push(xy);
    }

    //debugger

    var swingChart = new Chart(ctx, {
      data: {
      // labels: xLabels,
      datasets: []
      },
      options: {
          responsive: true,
          maintainaspectratio: false,
        scales: {
          x: {
            type: 'time',
            time: {
              parser: 'yyyy-MM-dd HH:mm',
            },
            scaleLabel: {
              display: true,
              labelString: 'Date'
            }
          },
          y: {
            scaleLabel: {
              display: true,
              labelString: 'value'
            }
          }
        }
      }
    });
    
    for (i= 0; i < vLabels.length; i++ ) {
      swingChart.data.datasets.push({
      label: vLabels[i], 
      type: "line",
      borderColor: '#'+(0x1100000+Math.random()*0xffffff).toString(16).substr(1,6),
      backgroundColor: "rgba(249, 238, 236, 0.74)",
      data: vData[i],
      spanGaps: true
      });
      swingChart.update();
    }
}
})

