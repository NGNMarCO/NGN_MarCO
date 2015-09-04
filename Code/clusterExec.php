<?php
// The clusterExec.php is used in index.php file (similar to layerCreator.php) in order to upload data into database
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

// EXECUTE THE PYTHON SCRIPT WHICH MAKES THE CLUSTERING AND THE NETWORK DESIGN (THANASIS CODE)
$command = "python ./python/clusterModule.py $numberOfClusters $shapeFilePath";
exec($command,$out,$ret);
print_r($out);
//print_r($ret);


// PASS THE SHAPE FILE OF THE CLUSTERS INTO THE DATABASE "ESOTERIKO" IN A TABLE WITH THE SAME NAME OF THE GENERATED SHAPEFILE (clusterNodes_)
$command = 'shp2pgsql -s 2100 -d /home/enomix/www/MarCO/Code/python/output/cluster/clusterNodes_.shp  | psql -h localhost -p 5432 -d esoteriko -U postgres';
exec($command,$out,$ret);
//print_r($out);
//print_r($ret);


// DELETE PREVIOUS LAYER FROM GEOSERVER (USE OF GEOSERVER API)/RELOAD THE CONF OF GEOSERVER (NECESSARY)/CREATE LAYER/ASSIGN STYLE TO THIS LAYER
// DELETE LAYER
$command = 'curl -v -u admin:geoserver -X DELETE "http://localhost:8080/geoserver/rest/layers/clusternodes_.xml"';
exec($command,$out,$ret);
		
// RELOAD CONF
$command = 'curl -v -u admin:geoserver -X PUT http://localhost:8080/geoserver/rest/reload';
exec($command,$out,$ret);
			
// CREATE LAYER
$command = 'curl -v -u admin:geoserver -X POST -H "Content-type: text/xml" -d "<featureType><name>clusternodes_</name></featureType>" http://localhost:8080/geoserver/rest/workspaces/esoteriko/datastores/esoteriko/featuretypes';
exec($command,$out,$ret);
		
// ASSIGN STYLE
$command = 'curl -u admin:geoserver -X PUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>cluster_new</name><workspace>esoteriko</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/esoteriko:clusternodes_';
exec($command,$out,$ret);
#echo var_dump($output);
?>


