//  this is for dynamically loading i json data every x seconds. 
    
//  https://stackoverflow.com/questions/49432579/await-is-only-valid-in-async-function 
// we can do this with every data, also json files

// all tags related to the image url
const previous_image = document.getElementById("previous_image")
previous_image.addEventListener("click", prev);
const next_image = document.getElementById("next_image")
next_image.addEventListener("click", next);


i = 0
function prev() {
	i = Math.min(i+1,50)
	  document.getElementById("img").src =`./images/output_${i}.jpg`
	  }
function next() {
	i = Math.max(i-1,0)
	  document.getElementById("img").src =`./images/output_${i}.jpg`
	  }


// all tags related to dynamic time data
const dynamic_time_data = document.getElementById("dynamic_time_data")
const n_images = document.createElement('div')
n_images.id = 'test'
const last_updated = document.createElement('div')
last_updated.id = 'last_updated'

dynamic_time_data.appendChild(n_images);
dynamic_time_data.appendChild(last_updated);

// all tags related to static data
const static_data = document.getElementById("static_data")
const area = document.createElement('div')
area.id = 'area'
const volume = document.createElement('div')
volume.id = 'volume'
const geo_location = document.createElement('div')
geo_location.id = 'location'
const current_percentage = document.createElement('div')
current_percentage.id = 'current_percentage'
const startdate = document.createElement('div')
startdate.id = 'startdate'
const stopdate = document.createElement('div')
stopdate.id = 'stopdate'
const upload_frequency = document.createElement('div')
upload_frequency.id = 'upload_frequency'



static_data.appendChild(area);
static_data.appendChild(volume);
static_data.appendChild(geo_location);
static_data.appendChild(current_percentage);
static_data.appendChild(startdate);
static_data.appendChild(stopdate);
static_data.appendChild(upload_frequency);

// all tags related to dynamic sensordata from houdini

// all tags related to static data
const dynamic_sensor_data = document.getElementById("dynamic_sensor_data")
const temperature = document.createElement('div')
temperature.id = 'temperature'
const humidity = document.createElement('div')
humidity.id = 'volume'
const proximity = document.createElement('div')
proximity.id = 'location'


dynamic_sensor_data.appendChild(temperature);
dynamic_sensor_data.appendChild(humidity);
dynamic_sensor_data.appendChild(proximity);


window.onload = function () { 	
	reloadJson("./js/dynamic_time_data.json")
	reloadImg("./images/output_0.jpg") 
	pastSeconds("./js/dynamic_time_data.json") 
	// load static json functions
	loadStaticJson("./js/static_data.json")
	// load dynamic sensor data functions
	loadSensorData("./js/dynamic_sensor_data.json")
}


reload_time = 10000

const reloadImg = url =>
  fetch(url, { cache: 'reload', mode: 'no-cors' })
  	.then((response) => {
  	if (!response.ok) {
 		
 		        fetch("./images/output_1.jpg", { cache: 'reload', mode: 'no-cors' })
 		        	.then((response) => { response.text();})
 		          	.then(() => document.getElementById("img").src ="./images/output_1.jpg")      
  		}
  	})
    .then(() => document.getElementById("img").src =url)


const reloadJson = url =>
  fetch(url, { cache: 'reload', mode: 'no-cors' })
  	.then((response) => {
  		if (response.ok) {
  			return response.json();
  		}
  	})
  	.then((json) => { 
  	
  	for(let data in json.time_data){
  		n_images.innerHTML =json.time_data.n_images + " rendered images"
  		status.innerHTML = json.time_data.status  + " % complete"
  	}
  }

  );

 
  const pastSeconds = url =>
    fetch(url, { cache: 'reload', mode: 'no-cors' })
    	.then((response) => {return response.json();})
    	.then((json) => { 
    		last_updated.innerHTML =  Math.round(Date.now()*1e-3) - json.time_data.last_updated + " seconds past since last update"
    }
  );


  // all static json files fom static_data.json are here
 
  const loadStaticJson = url =>
    fetch(url, { cache: 'reload', mode: 'no-cors' })
    	.then((response) => {
    		if (response.ok) {
    			return response.json();
    		}	
    	})
    	.then((json) => { 
			area.innerHTML = json.size.area
			volume.innerHTML = json.size.volume
			geo_location.innerHTML = json.location.city

			const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

			startdate.innerHTML = 'begindate: '+json.timing.startdate[2] + 'th of '+ months[json.timing.startdate[1]] + ' '+  json.timing.startdate[0]
			stopdate.innerHTML ='enddate: '+  json.timing.stopdate[2] + 'th of '+ months[json.timing.stopdate[1]] + ' '+  json.timing.stopdate[0]
			const currentTime = new Date().getTime()
			const startTime = new Date(json.timing.startdate[0], json.timing.startdate[1], json.timing.startdate[2]).getTime()
			const stopTime = new Date(json.timing.stopdate[0], json.timing.stopdate[1], json.timing.stopdate[2]).getTime()
			
			const current_processed_percentage = Math.max(Math.min(Math.round((currentTime -startTime)/(stopTime -startTime ) *100),100),0)
			current_percentage.innerHTML =current_processed_percentage + '% of the data is processed'
			
			upload_frequency.innerHTML = json.timing.upload_frequency
    	}
    );



   // all dynamic_sensor_data.json files are here
 
  const loadSensorData = url =>
    fetch(url, { cache: 'reload', mode: 'no-cors' })
    	.then((response) => {
    		if (response.ok) {
    			return response.json();
    		}	
    	})
    	.then((json) => { 
			temperature.innerHTML ="the average temperature is: " + json.sensor_data.temperature + "°C"
			humidity.innerHTML ="the average humidity is: " + Math.round(json.sensor_data.humidity*10)/100 + "% humidity"
			proximity.innerHTML = "the average proximity is: " +Math.round(json.sensor_data.proximity*100)/100 + " units"		
    	}
    );

setInterval(function(){
	reloadJson("./js/dynamic_time_data.json")
 	reloadImg("./images/output_0.jpg")
	// dynamic sensor data functions
 	loadSensorData("./js/dynamic_sensor_data.json")
}, reload_time);

setInterval(function(){
	fetch("./js/dynamic_time_data.json", { cache: 'reload', mode: 'no-cors' })
	    	.then((response) => {return response.json();})
	    	.then((json) => { 
	    		last_updated.innerHTML =  Math.max((Math.round(Date.now()*1e-3) - json.time_data.last_updated -3),0) + " seconds past since last update"
	    }
	  );
}, 1000);
