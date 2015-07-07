<?php
ini_set('display_errors', 1);

include '_postgresConnect.php';

# READ CSV FILE


# PASS VARIABLES FROM FORM
$numberOfClusters = $_POST['numberOfClusters'];
$shapeFilePath = $_POST['shapeFilePath'];
$capList = $_POST['capList'];
$cap_list_cost = $_POST['capListCost'];
$KVcost = $_POST['KVcost'];
$lmin = $_POST['lmin'];
$lmax = $_POST['lmax'];
$mhn_cost = $_POST['mhn_cost'];

// EXECUTE THE PYTHON SCRIPT WHICH MAKES THE CLUSTERING AND THE NETWORK DESIGN (THANASIS CODE)
$output = exec("python ./marCO/src/main_testing_2.py $numberOfClusters $shapeFilePath $capList $cap_list_cost $KVcost $lmin $lmax $mhn_cost");
echo($output);



// PASS THE SHAPE FILE OF THE CLUSTERS INTO THE DATABASE "ESOTERIKO" IN A TABLE WITH THE SAME NAME OF THE GENERATED SHAPEFILE (clusterNodes_)
$command = 'shp2pgsql -s 2100 -d /home/enomix/www/MarCO/MarCO/tryingbootstrap/RunPythonThroughPHP/marCO/src/outputDistributionStuff/cluster/clusterNodes_.shp  | psql -h localhost -p 5432 -d esoteriko -U postgres';
exec($command,$out,$ret);
print_r($out);
print_r($ret);


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


