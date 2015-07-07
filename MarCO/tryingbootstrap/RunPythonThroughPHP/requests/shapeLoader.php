<?php
ini_set('display_errors', 1);

include '_postgresConnect.php';

# READ CSV FILE


# PASS VARIABLES FROM FORM
$shapeName = $_POST['shapeName'];
// remove data type
$start = 0;
$layerInd =strpos($shapeName,'.'); // layer name for geoserver
$layerName = strtolower(substr($shapeName, $start, $layerInd)); // lower casing so it fits with postgis
//print_r($layerName);

//print_r($shapeName);


/*
// PASS THE SHAPE FILE OF THE CLUSTERS INTO THE DATABASE "ESOTERIKO" IN A TABLE WITH THE SAME NAME OF THE GENERATED SHAPEFILE (clusterNodes_)
$command = "shp2pgsql -s 2100 -d /home/enomix/www/MarCO/MarCO/tryingbootstrap/RunPythonThroughPHP/marCO/src/outputDistributionStuff/$shapeName | psql -h localhost -p 5432 -d esoteriko -U postgres";
exec($command,$out,$ret);
//print_r($command);
//print_r($ret);
*/

/*
// DELETE PREVIOUS LAYER FROM GEOSERVER (USE OF GEOSERVER API)/RELOAD THE CONF OF GEOSERVER (NECESSARY)/CREATE LAYER/ASSIGN STYLE TO THIS LAYER
// DELETE LAYER
$command = 'curl -v -u admin:geoserver -X DELETE "http://localhost:8080/geoserver/rest/layers/clusternodes_.xml"';
exec($command,$out,$ret);
*/

// RELOAD CONF
$command = 'curl -v -u admin:geoserver -X PUT http://localhost:8080/geoserver/rest/reload';
//print_r($command);
exec($command,$out,$ret);
	
		
// CREATE LAYER
$command = 'curl -v -u admin:geoserver -X POST -H "Content-type: text/xml" -d "<featureType><name>'.$layerName.'</name></featureType>" http://localhost:8080/geoserver/rest/workspaces/esoteriko/datastores/esoteriko/featuretypes';
//print_r($command);
exec($command,$out,$ret);

/*	
// ASSIGN STYLE
$command = 'curl -u admin:geoserver -X PUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>cluster_new</name><workspace>esoteriko</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/esoteriko:clusternodes_';
exec($command,$out,$ret);
*/
	
		
echo $layerName;
?>


