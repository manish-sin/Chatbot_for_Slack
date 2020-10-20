document.addEventListener('DOMContentLoaded', ()=>{
	/* var socket = io.connect('http://localhost:5000'); */
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	
	socket.on('connect', () => {
		socket.send("I am connected");
	})


	socket.on('message', data=> {
		// <!-- var variable1 = localStorage.getItem("vOneLocalStorage "); */ -->
		console.log(`Message received: first message`)
		console.log(`Message received: ${data};`)
		console.log(`Total Msg count: ${data[0]};`)
		for (i = 1; i < data[0]+1; i++) {
         console.log(`Message No.  : ${data[i]};`)
        }



	/* #const data = data */
	var color = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]

	var pie_chart = new Chart(document.getElementById("pie-chart"), {
		type: 'pie',
		data: {
		  labels: data[2],
		  datasets: [{
			
			backgroundColor: color,
			data: data[1]
		  }]
		},
		options: {
		  title: {
			display: true,
			text: 'Incident Summary Report - Product Wise'
		  }
		}
	});
	console.log(data)

    var a=[]
	for (var i = 0; i<data[4]; i++){
	 var b = {
          label: data[6][i],
          backgroundColor: color[i],
          data: data[7+i]
        }
	a.push(b)
	}
	

    
	var bar_chart = new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: data[3],
      datasets: a
    },
    options: {
      title: {
        display: true,
        text: 'Incident Summary Report User-wise'
      }
        /* scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
    } */
	}
    
});

    var e = 0

	var c=[]
	for (var i = 0; i<data[4]; i++){
	 e = +data[4]+7+i;
	 console.log(typeof(e))
	 console.log(`Total Msg count: ${e};`);
	 var d = {
          label: data[6][i],
          borderColor: color[i],
          data: data[e],
          fill: false
        }
	c.push(d)
	}
new Chart(document.getElementById("mixed-chart"), {
    type: "line",
    data: {
      labels: data[5],
      datasets: c
    },
    options: {
      title: {
        display: true,
        text: 'Incident Summary Report Timeline'
      },
      legend: { display: false }
    }
});


	
});
	}); 