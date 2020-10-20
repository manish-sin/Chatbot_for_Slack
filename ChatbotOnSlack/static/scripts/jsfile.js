document.addEventListener('DOMContentLoaded', ()=>{
	var socket = io.connect('http://localhost:5000');

	socket.on('connect', () => {
		socket.send("I am connected");
	})


	socket.on('message', data=> {
		<!-- var variable1 = localStorage.getItem("vOneLocalStorage "); */ -->
		console.log(`Message received: ${data};`)
		
		console.log(`Message received: ${data[0]};`)
		console.log(`Message received: ${data[1]};`)
	/* #const data = data */
	
	
	new Chart(document.getElementById("pie-chart"), {
		type: 'pie',
		data: {
		  labels: data[1],
		  datasets: [{
			label: "Population (millions)",
			backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
			data: data[0]
		  }]
		},
		options: {
		  title: {
			display: true,
			text: 'Query Summary Report - Product Wise'
		  }
		}
	});
/* <!--    Our labels along the x-axis-->
    var years = [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050];
<!--    // For drawing the lines-->
    var africa = [86,114,106,106,107,111,133,221,783,2478];
    var asia = [282,350,411,502,635,809,947,1402,3700,5267];
    var europe = [168,170,178,190,203,276,408,547,675,734];
    var latinAmerica = [40,20,10,16,24,38,74,167,508,784];
    var northAmerica = [6,3,2,2,7,26,82,172,312,433];
 */
    /* var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: years,
        datasets: [
          {
			  data: africa,
			  label: "Africa",
			  borderColor: "#3e95cd",
			  fill: false
			},
			{
			  data: asia,
			  label: "Asia",
			  borderColor: "#3e95cd",
			  fill: false
			},
			{
			  data: europe,
			  label: "Europe",
			  borderColor: "#3e95cd",
			  fill: false
			},
			{
			  data: latinAmerica,
			  label: "Latin America",
			  borderColor: "#3e95cd",
			  fill: false
			},
			{
			  data: northAmerica,
			  label: "North America",
			  borderColor: "#3e95cd",
			  fill: false
			}
        ]
      }
    });
*/
	});

	}); 