<?php

//**************************************************************
//
// Inserts output data into database
//										       														       
//**************************************************************
// ERROR MESSAGES
ini_set('display_errors', 1); 
// INCLUDE PHP FILES
include 'postgresConnect.php';
$scenario = $_POST['datastr'];
$VariableType = $_POST['VariableType'];
$TotalCost = $_POST['TotalCost'];

//MAKE POSTGIS QUERY TO SEE NEARBY KOMVOUS (images - komvoi)
//$resultKomvoi = pg_query($dbconn, "SELECT variable, num FROM spreadtest WHERE scenario='$scenario'");
$resultKomvoi = pg_query($dbconn, "INSERT INTO output(scenario, variable, num) VALUES('$scenario', '$VariableType', $TotalCost);");
$valuesArr = [];
while ($rowKomvoi = pg_fetch_row($resultKomvoi)) {
	echo "$rowKomvoi[1],";
}



?>

