<?php

//**************************************************************
//
//
//										       														       
//**************************************************************
// ERROR MESSAGES
ini_set('display_errors', 1); 
// INCLUDE PHP FILES
include 'postgresConnect.php';
$scenario = $_POST['datastr'];


//MAKE POSTGIS QUERY TO SEE NEARBY KOMVOUS (images - komvoi)
$resultKomvoi = pg_query($dbconn, "SELECT variable, num FROM spreadtest WHERE scenario='$scenario'");
$valuesArr = [];
while ($rowKomvoi = pg_fetch_row($resultKomvoi)) {
	echo "$rowKomvoi[1],";
}



?>

