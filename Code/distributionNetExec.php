<?php
// The distributionNetExec.php is used in index.php file (similar to layerCreator.php) in order to upload data into database
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
$capList = $_POST['capList'];
$cap_list_cost = $_POST['capListCost'];
$KVcost = $_POST['KVcost'];
$lmin = $_POST['lmin'];
$lmax = $_POST['lmax'];
$mhn_cost = $_POST['mhn_cost'];
$PercentageOfCoverageDHN = $_POST['PercentageOfCoverageDHN'];
$mhn_c_l = $_POST['mhn_c_l'];
$d = $_POST['d']; // type of strategy

// EXECUTE THE PYTHON SCRIPT WHICH MAKES THE CLUSTERING AND THE NETWORK DESIGN (THANASIS CODE)
$command = "python ./python/distributionNetModule.py $numberOfClusters $shapeFilePath $capList $cap_list_cost $KVcost $lmin $lmax $mhn_cost $PercentageOfCoverageDHN $mhn_c_l $d";

exec($command,$out,$ret);
print_r($out);
//print_r($ret);

?>


