<?php
ini_set('display_errors', 1);
# READ CSV FILE
# PASS VARIABLES FROM CSV 
$var1 = "1";
//$output = exec("python ./aa_scratch0/all.py");
$output = exec("python test.py $var1" );
echo var_dump($output);
?>

