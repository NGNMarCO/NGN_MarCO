<?php

//**************************************************************
//*	Connect to Postgres												       
//*														       
//**************************************************************
ini_set('display_errors', 1); 

/*
	$db = new PDO('pgsql:dbname=esoteriko;user=postgres;password=postgres;host=localhost;port=5432');
	$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
*/

$dbconn = pg_connect("host=localhost port=5432 dbname=esoteriko user=postgres password=postgres") or die('Could not connect: ' . pg_last_error());

if (!$dbconn) {
  echo "An error occurred.\n";
  exit;
}

?>

