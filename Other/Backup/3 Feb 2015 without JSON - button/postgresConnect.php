<?php

//**************************************************************
//*	Connect to Postgres												       
//*														       
//**************************************************************
ini_set('display_errors', 1); 
$dbconn = pg_connect("host=localhost port=5432 dbname=esoteriko user=postgres password=1249") or die('Could not connect: ' . pg_last_error());

if (!$dbconn) {
  echo "An error occurred.\n";
  exit;
}
?>

