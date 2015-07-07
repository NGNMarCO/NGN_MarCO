<?php

//**************************************************************
//
// Loads a shape file to a postgis database
//										       														       
//**************************************************************
// ERROR MESSAGES
ini_set('display_errors', 1); 
// INCLUDE PHP FILES
include 'postgresConnect.php';

$command = 'shp2pgsql -s 2100 -d /home/enomix/www/EsoterikoFinal/Maps/shps/last/axons_larissa_with_buildings6_sub0.shp  | psql -h localhost -p 5432 -d esoteriko -U postgres';
#$command = 'shp2pgsql -s 2100 -d /home/enomix/www/EsoterikoFinal/Maps/shps/last/axons_larissa_with_buildings6_sub0.shp  | psql -h localhost -p 5432 -d esoteriko -U postgres';
exec($command,$out,$ret);
print_r($out);
print_r($ret);


?>

