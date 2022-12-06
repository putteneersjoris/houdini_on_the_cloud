// <!-- this is for dynamically loading i json data every x seconds. -->
    
// <!-- https://stackoverflow.com/questions/49432579/await-is-only-valid-in-async-function -->
// we can do this with every data, also json files

window.onload = function () { 	
	reloadJson("./js/data.json")
	reloadImg("./images/output_0.jpg")  
}

reload_time = 10000

const reloadImg = url =>
  fetch(url, { cache: 'reload', mode: 'no-cors' })
  	.then((response) => {
  		if (response.ok) {
  			return response.text();
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
  	document.getElementById("data").innerHTML =json.data
	document.getElementById("n_img").innerHTML =json.n_img + ' images where renderered'
  }

  );

setInterval(function(){
	reloadJson("./js/data.json")
 	reloadImg("./images/output_0.jpg")
}, reload_time);
