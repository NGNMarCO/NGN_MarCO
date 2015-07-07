


<html lang="en">

<head>
	


</head>

<body>
		<ul class="nav">
        <li class="dropdown">
          <a class="dropdown-toggle" data-toggle="dropdown" href="#">
            <h4 style="color: #333333">Select a Sound -</h4> <b class="caret"></b>
          </a>

          <ul class="dropdown-menu">
            <?php foreach(glob("RunPythonThroughPHP/marCO/src/outputDistributionStuff/*.shp") as $filename){
				// GET INDEX
				$pos = strpos($filename, 'outputDistributionStuff/');
				// GET SUBSTRING WITH SHAPE NAME
				$rest = substr($filename, $pos+24);    
				echo "<li>".$rest."</li>";
            }
            ?>
          </ul>
        </li>
	</ul>
	
</body>


</html>










<?php 
/*
// ERROR MESSAGES
ini_set('display_errors', 1); 
// GET THE SHAPE FILES IN THIS PATH
foreach(glob("RunPythonThroughPHP/marCO/src/aa_scratch0/*.shp") as $filename){  
	// GET INDEX
			  $pos = strpos($filename, 'aa_scratch0/');
			  // GET SUBSTRING WITH SHAPE NAME
			  $rest = substr($filename, $pos+12);    
			echo $rest;
	
          }
*/
?>
