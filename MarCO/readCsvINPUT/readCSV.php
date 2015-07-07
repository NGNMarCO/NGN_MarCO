<?php

//**************************************************************
//*	Reads the CSV file with Inputs												       
//*														       
//**************************************************************
ini_set('display_errors', 1); 

$file = fopen("input_data.csv","r");

fgetcsv($file);

while(! feof($file)){ // check if the end of the file is reached
	$ar=fgetcsv($file,0,";"); // determine the delimeter
	echo print_r($ar); // print the array 
	echo "<br>";
}
fclose($file);


?>


