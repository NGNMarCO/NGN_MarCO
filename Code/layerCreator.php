<?php
// The layer creator is used in _map.php file in order to create layers in Geoserver (using geoserver API)
// and display them on the map. The following steps are executed: 1) reload (refresh) geoserver 
// 2) create a new layer 
ini_set('display_errors', 1);
include '_postgresConnect.php';

# PASS VARIABLES FROM FORM
$shapeName = $_POST['shapeName'];
// remove data type
$start = 0;
$layerInd =strpos($shapeName,'.'); // layer name for geoserver
$layerName = strtolower(substr($shapeName, $start, $layerInd)); // lower casing so it fits with postgis



// PASS THE SHAPE FILE INTO THE DATABASE "ESOTERIKO" IN A TABLE WITH THE SAME NAME OF THE GENERATED SHAPEFILE (clusterNodes_)
$command = "shp2pgsql -s 2100 -d /home/enomix/www/MarCO/Code/python/output/DistributionNetwork/$shapeName | psql -h localhost -p 5432 -d esoteriko -U postgres";
exec($command,$out,$ret);
//print_r($command);
//print_r($ret);

// DELETE PREVIOUS LAYER FROM GEOSERVER (USE OF GEOSERVER API)
$command = 'curl -v -u admin:geoserver -X DELETE "http://localhost:8080/geoserver/rest/layers/'.$layerName.'"';
exec($command,$out,$ret);


// RELOAD CONF
$command = 'curl -v -u admin:geoserver -X PUT http://localhost:8080/geoserver/rest/reload';
//print_r($command);
exec($command,$out,$ret);
		
// CREATE LAYER
$command = 'curl -v -u admin:geoserver -X POST -H "Content-type: text/xml" -d "<featureType><name>'.$layerName.'</name></featureType>" http://localhost:8080/geoserver/rest/workspaces/esoteriko/datastores/esoteriko/featuretypes';
//print_r($command);
exec($command,$out,$ret);

//print_r($out);
echo $layerName;
?>


