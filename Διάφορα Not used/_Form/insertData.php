<?php

//**************************************************************
//
// Inserts output data into database
//										       														       
//**************************************************************
// ERROR MESSAGES
ini_set('display_errors', 1); 
//include 'postgresConnect.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST'){

	$db = new PDO('pgsql:dbname=esoteriko;user=postgres;password=postgres;host=localhost;port=5432');
	$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	// GET VARIABLES TO BE PASSED
	//$postdata = file_get_contents("php://input");
	//echo($postdata);
	
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


	if ($db) {
		$stmt = $db->prepare("INSERT INTO inputs(CentralOffices, DistributionCenter, Method, Tech, BrownGreen, 
						InfustructureType, NumberSubDuctsFeeder, NumberSubDuctsDistribution, CableGranulFeeder,CableGranulDistribution,ManholeStrategyFeeder,
						ManholeStrategyDistribution, Percentages, ScenarioName, ScenarioDescription ) 
						VALUES(:CentralOffices, :DestributionCenter, :Method, :Tech, :BrownGreen, :InfustructureType, :NumberSubDuctsFeeder, :NumberSubDuctsDistribution,
						 :CableGranulFeeder, :CableGranulDistribution,:ManholeStrategyFeeder,:ManholeStrategyDistribution, :Percentages, :ScenarioName,:ScenarioDescription );");

		$stmt->execute(array('CentralOffices' => $CentralOffice,'DestributionCenter' => $DestributionCenter,'Method' => $Method,'Tech' => $Tech,'BrownGreen' => $BrownGreen,
							'InfustructureType' => $InfustructureType,'NumberSubDuctsFeeder' => $NumSubDucFeeder,
							'NumberSubDuctsDistribution' => $NumSubDucDistrib,'CableGranulFeeder' => $CableGranFeeder,'CableGranulDistribution' => $CableGranDistrib
							,'ManholeStrategyFeeder' => $ManholeFeederArrStr,'ManholeStrategyDistribution' => $ManholeDistribArrStr,'Percentages' => $Percentages,'ScenarioName' => $ScenarioName,'ScenarioDescription' => $ScenarioDescription));
		pg_close($db); // close connection
	}
}


?>

