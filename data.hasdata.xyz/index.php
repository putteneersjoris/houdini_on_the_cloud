<?php
$servername = "localhost";
$username = "root";
$password = "Gj1*uFW?Hhfuh44n";
$dbname = "data";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
}



if ('PUT' === $_SERVER['REQUEST_METHOD']) {
	echo "this is a put request\n";

	parse_str(file_get_contents("php://input"),$post_vars);
	$_PUT = json_decode(file_get_contents('php://input'), true);

	echo $_PUT['id']."\n";
	echo $_PUT['sensorID']."\n";
	echo $_PUT['type']."\n";
	echo $_PUT['metric']."\n";
	echo $_PUT['value']."\n";
	echo $_PUT['time']."\n";


//add to sensordata table
if (array_key_exists("id",$_PUT) && array_key_exists("sensorID",$_PUT) && array_key_exists("type",$_PUT) && array_key_exists("metric",$_PUT) && array_key_exists("value",$_PUT) && array_key_exists("time",$_PUT) )
{  	    
	  $sql = "INSERT INTO sensordata VALUES ({$_PUT['id']},'{$_PUT['sensorID']}', {$_PUT['type']}, {$_PUT['metric']},{$_PUT['value']},'{$_PUT['time']}' )";
	  if ($conn->query($sql) === TRUE) {
	  	echo "New record created successfully";
	   }
	   else {
	   echo "Error: " . $sql . "<br>" . $conn->error;
	   }
	}
}



if ('GET' === $_SERVER['REQUEST_METHOD']) {
	$queries = array();
	parse_str($_SERVER['QUERY_STRING'], $queries);
	
	
	$sensorID_query = is_numeric($queries['sensorID']) ? "=".$queries['sensorID'] : ">-1";
	$sensorData_query = ['*' => "",
	'luminosity' => "AND type=1 AND metric=0", //sensor 1
	'temperature' => "AND type=2 AND metric=2",'humidity' => "AND type=2 AND metric=1",  //sensor2
	'proximity' => "AND type=3 AND metric=0",  //sensor 3
	'co' => "AND type=4 AND metric=1", 'voc' => "AND type=4 AND metric=2",  //sensor 4
		];



	 // $sql = "SELECT ".$queries['show']. " FROM sensordata WHERE ( sensorID ".$sensorID_query."  ".  $sensorData_query[$queries['data']]. "  ) LIMIT ". $queries['limit']."" ;

	 $sql = "SELECT  ".$queries['show']. " FROM 
	 					( SELECT  * FROM sensordata WHERE(sensorID ".$sensorID_query." ".  $sensorData_query[$queries['data']]. " )
						ORDER BY id DESC LIMIT ". $queries['limit']." )tmp ORDER BY tmp.id ASC";

	// see all values from all sensors
	// http://data.hasdata.xyz/?show=*&sensorID=*&data=*&limit=100

	// show the sensorID value for all sensors
	// http://data.hasdata.xyz/?show=sensorID&sensor_id=*&data=*&limit=100

	// show all data and time values for sensor 0
	// http://data.hasdata.xyz/?show=value,time&sensorID=0&data=*&limit=100

	// see temperature value and time for sensor 1
	// http://data.hasdata.xyz/?show=value,time&sensorID=1&data=temperature&limit=100

	// how to see value and sensorID from all sensors who are measuring luminosity
	// http://data.hasdata.xyz/?show=value,sensorID&sensorID=*&data=luminosity&limit=100

	// see luminosity values for sensor 0
	// http://data.hasdata.xyz/?show=value&sensorID=0&data=luminosity&limit=100

	// see luminosity data for sensor 3
	// http://data.hasdata.xyz/?show=value&sensorID=3&data=luminosity&limit=100

	// see all sensorid s of sensors measuring temperature
	// http://data.hasdata.xyz/?show=sensorID&sensorID=*&data=temperature&limit=100

    // show last 7 luminosity measurementas from value, time and id
	// http://data.hasdata.xyz/?show=value,time,id&sensorID=*&data=luminosity&limit=7

	// show last 5 results from sensor 0
	// http://data.hasdata.xyz/?show=*&sensorID=0&data=*&limit=5

	
	$res = $conn->query($sql);
	$rows = $res->fetch_all(MYSQLI_ASSOC);

	if(array_key_exists('last', $queries)){
		echo json_encode($rows[0]);
	}
	else{
		echo json_encode($rows);
	}
	$conn->close();
}

?>	
																	
