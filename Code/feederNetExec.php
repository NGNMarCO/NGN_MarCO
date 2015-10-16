<?php
// The feederNetExec.php is used in index.php file (similar to layerCreator.php) in order to upload data into database
// and create cluster layer in Geoserver (using geoserver API)
// and display them on the map. The following steps are executed: 1) the newly generated shapefile with the cluster
// (from the Python code) is passed into a table in database (replaces previous data). 2)The previous layer in geoserver
// is deleted 3) reload (refresh) geoserver 4) create a new layer 5) assign styles on this layer (colors etc.) Not used currently.
// Current state:..
ini_set('display_errors', 1);
include '_postgresConnect.php';


# PASS VARIABLES FROM FORM
$numberOfClusters = $_POST['numberOfClusters'];
$shapeFilePath = $_POST['shapeFilePath'];
$capListFeeder = $_POST['capListFeeder'];
$capListCostFeeder = $_POST['capListCostFeeder'];
$CentralOfficecost = $_POST['CentralOfficecost'];
$lminFeeder = $_POST['lminFeeder'];
$lmaxFeeder = $_POST['lmaxFeeder'];
$mhn_costFeeder = $_POST['mhn_costFeeder'];
$mhn_c_l_feeder = $_POST['mhn_c_l_feeder'];
$d = $_POST['d_feeder'];
$PercentageOfCoverageDHN = $_POST['PercentageOfCoverageDHN'];
$COname = $_POST['COname'];
$scenarioName = $_POST['scenarioName'];


// EXECUTE THE PYTHON SCRIPT WHICH MAKES THE CLUSTERING AND THE NETWORK DESIGN (THANASIS CODE)
$command = "python ./python/centralOfficeModule.py $numberOfClusters $shapeFilePath $capListFeeder $capListCostFeeder $CentralOfficecost $lminFeeder $lmaxFeeder $mhn_costFeeder $mhn_c_l_feeder $d $PercentageOfCoverageDHN $COname $scenarioName";
exec($command,$out,$ret);

print_r($out);
print_r($ret);


?>


