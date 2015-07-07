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


// GET VARIABLES TO BE PASSED

$CentralOffice = $_POST['CentralOffice'];
$DestributionCenter = $_POST['DestributionCenter'];
$Method = $_POST['Method'];
$Tech = $_POST['Tech']; 
$BrownGreen = $_POST['BrownGreen'];
$InfustructureType = $_POST['InfustructureType'];
$NumSubDucFeeder = $_POST['NumSubDucFeeder'];
$NumSubDucDistrib = $_POST['NumSubDucDistrib'];
$CableGranFeeder = $_POST['CableGranFeeder']; 
$CableGranDistrib = $_POST['CableGranDistrib'];
$ManholeFeederArrStr = $_POST['ManholeFeederArrStr'];
$ManholeDistribArrStr = $_POST['ManholeDistribArrStr'];
$Percentages = $_POST['Percentages'];
$ScenarioName = $_POST['ScenarioName'];
$ScenarioDescription = $_POST['ScenarioDescription'];

$insertData = pg_query($dbconn, "INSERT INTO inputs(CentralOffices, DistributionCenter, Method, Tech, BrownGreen, InfustructureType, NumberSubDuctsFeeder, NumberSubDuctsDistribution, CableGranulFeeder,CableGranulDistribution,ManholeStrategyFeeder,ManholeStrategyDistribution, Percentages, ScenarioName, ScenarioDescription ) 
VALUES('$CentralOffice', '$DestributionCenter', '$Method', '$Tech', '$BrownGreen', '$InfustructureType', '$NumSubDucFeeder', '$NumSubDucDistrib', '$CableGranFeeder', '$CableGranDistrib','$ManholeFeederArrStr','$ManholeDistribArrStr', '$Percentages', '$ScenarioName','$ScenarioDescription' );");
$valuesArr = [];
while ($importedData = pg_fetch_row($insertData)) {
	echo "$importedData[1],";
}


?>

