<!DOCTYPE html>
<!-- 3rd party tools used: BootstrapCSS, OpenLayers, 
Short Description: _map.php consists of two parts. 1) The shape loader, which reads all the 
available shape files inside a specified folder and through a dropdown menu you can select any of
them and 2) the map, which displays all the generated data (nodes and edges) created by the 
algorithm (white cross on the right of the map).
Current state: To display the data we use geoserver (localhost). We use the Geoserver API in order to 
create the layers (with the points and lines) on real time (See layerCreator.php)
Improvements: 1) The user can add more than once the same layer just by selecting the shapefile name from the 
shape file loader. This should prevented. 2) In some cases the newly generated cluster layers are not displayed 
correctly on the map; This can be related with the cache of the browser.
-->
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <!-- Bootstrap Core CSS -->
    <link href="Libs/BootStrapCSS/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="Libs/BootStrapCSS/css/sb-admin.css" rel="stylesheet">
    <!-- Custom Fonts -->
    <link href="Libs/BootStrapCSS/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
	<!-- Load Openlayers - openlayers 2.13 cause issue with geoserver-->
	<script src="Libs/OpenLayers-2.12/OpenLayers.min.js"></script>
	<!-- OpenLayers -->
	<script  type="text/javascript">
		var map;
		var osm;
		
		// Function: init()
		// Description: Is executed on body load. Creates the map and add a layer on it.
		function init(){
				map = new OpenLayers.Map({
				div: "map"
			});
			osm = new OpenLayers.Layer.OSM(); //osm: open street map
			// Define a Layer for the map (the layer is also declared in Geoserver localhost)	
			wms_layer_larisa =  new OpenLayers.Layer.WMS( "Larisa","http://localhost/geoserver/gwc/service/wms",
				{
					"layers": 'esoteriko:clusternodes_', // workspace and layer name in geoserver
					"format":  "image/png",
					"transparent": true,
					"version": "1.1.1",
					tiled: true,
					
				},
				{
					format: "image/png",
					displayOutsideMaxExtent: false,
					projection: new OpenLayers.Projection("EPSG:900913"), // map projection
				}
			);
			map.addLayers([wms_layer_larisa,osm]); // add the layers on the map
			// SET CORRECT PROJECTION FOR LAYERS - CENTER AND ZOOM LEVEL (7)
			var lonLat = new OpenLayers.LonLat(22.421743,39.626646).transform(new  OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
			map.setCenter (lonLat, 13);
			map.addControl(new OpenLayers.Control.LayerSwitcher()); // add controls on the map
		};
		
		// Function: loader()
		// Input: the name of the layer (string)
		// Description: Takes the name of the layer and adds it on the map
		function loader(layerName){
			var indexLayer = layerName.indexOf(":");
			var layerName = layerName.substring(indexLayer+1);
			var layerName = $.trim(layerName); // trim whitespaces
			var workspace = 'esoteriko:';
			var layerName2 = String('esoteriko:'.concat(layerName));	
			//alert(layerName2);
			// ADD THE LAYER OPENLAYERS
			wms_layer_larisa2 =  new OpenLayers.Layer.WMS(layerName,"http://localhost/geoserver/gwc/service/wms",
				{
					"layers": layerName2,
					"format":  "image/png",
					"transparent": true,
					"version": "1.1.1",
					"tiled": true	
				},
				{
					format: "image/png",
					displayOutsideMaxExtent: false,
					projection: new OpenLayers.Projection("EPSG:900913"),
				}
			);			
			map.addLayer(wms_layer_larisa2);	
		}
      </script>
</head>

<body onload=init()>
    <div id="wrapper">
        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
            </div>
            <!-- Top Menu Items -->
            <ul class="nav navbar-right top-nav">
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="fa fa-user"></i> MarCO <b class="caret"></b></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="#"><i class="fa fa-fw fa-user"></i> Profile</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-fw fa-gear"></i> Settings</a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#"><i class="fa fa-fw fa-power-off"></i> Log Out</a>
                        </li>
                    </ul>
                </li>
            </ul>
            <!-- Sidebar Menu Items - These collapse to the responsive navigation menu on small screens -->
            <div class="collapse navbar-collapse navbar-ex1-collapse">
                <ul class="nav navbar-nav side-nav">
					<li>
                        <a href="_indexx.php"><i class="fa fa-fw fa-edit"></i> Input Form</a>
                    </li>
                    <li>
                        <a href="_spreadsheet.html"><i class="fa fa-fw fa-table"></i> Excel</a>
                    </li>
                    
                    <li class="active">
                        <a href="_map.php"><i class="fa fa-fw fa-map-marker"></i> Map</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </nav>
        <div id="page-wrapper">
            <div >
                <!-- Page Heading -->
                <div class="row">
                    <div class="col-lg-12">	
                        <ol class="breadcrumb">
                            <li>
                                <i class="fa fa-dashboard active"></i>  <a href="_indexx.html">Input Form</a>
                            </li>
                        </ol>	
                    </div>
                </div>
                <!-- /.row -->
			<div class="row">
				<div class="col-lg-12">
						<div class="panel panel-success">
							<div class="panel-heading">
								<h3 class="panel-title"><i class="fa fa-table"></i> Shape File Loader</h3>
							</div>
							<div class="panel-body"  style="height:100%">
								<div class="form-group" >
									<!-- DROPDOWN MENU LISTING ALL SHAPE FILES -->
									<div class="input-group">
										<div class="input-group-btn">
											<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
												Select Shape File
												<span class="caret"></span>
											</button>
											<ul id="dropdown-menu-id" class="dropdown-menu" role="menu">
												<?php foreach(glob("Code/python/output/DistributionNetwork/*.shp") as $filename){
													// GET INDEX
													$pos = strpos($filename, 'output/');
													// GET SUBSTRING WITH SHAPE NAME
													$rest = substr($filename, $pos+27);
													echo "<li class='demolist'><a href=>".$rest."</a></li>";   
												}?>
											</ul>	
										</div>
										<!-- /btn-group -->
										<input type="text" class="form-control" id="inputShp" placeholder="Shape File Path" data-toggle="tooltip" title="Shape file path">		
									</div>
									<!-- /input-group -->
								</div>				
							</div>
						</div>
					</div>	
				</div>
				<!-- /.row -->
				<div class="row">
					<div class="col-lg-12" style="height:100%">
						<div class="panel panel-success">
							<div class="panel-heading">
								<h3 class="panel-title"><i class="fa fa-table"></i> Map</h3>
							</div>
								<div class="panel-body"  style="height:100%">
										<div  id="map"  style="width:100%; height:500px;"</div>
								</div>	
							</div>					    
						</div> 	 				    
					</div>    
				</div>
            </div>
            <!-- /.container-fluid -->
        </div>
        <!-- /#page-wrapper -->
    </div>
    <!-- /#wrapper -->
    
    <!-- Load Libraries -->
	<!-- jQuery -->
    <script src="Libs/BootStrapCSS/js/jquery.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="Libs/BootStrapCSS/js/bootstrap.min.js"></script>
	
	 <!-- Shape File Loader -->
	<script>	
		$(document).ready(function(){
			$('.demolist').on('click', function(){
				var shapeName =  $(this).find("a").text(); // GET THE VALUE OF DROPDOWN MENU AND PLACE IT TO TEXTFIELD
				//alert(shapeName);
				var wholePath = 'Code/python/output/DistributionNetwork/'+shapeName;
				$('#inputShp').val(wholePath);
				 $("#dropdown-menu-id").dropdown("toggle"); // CLOSE THE DROPDOWN MENU AFTER SELECTION 
				 // MAKE AJAX REQUEST TO PASS SHAPE FILE
				 $.ajax({
					type: "POST",
					url: 'Code/layerCreator.php',
					data: {shapeName:shapeName }, // PASS THE NAME OF THE SHAPE FILE - WHICH WILL BE THE NAME OF THE TABLE
					success: function(layerName){
						//alert(layerName);
						var layerName =  'esoteriko:'.concat(layerName);
						//alert(layerName);
						// LOADS THE NEWLY GENERATED LAYER - function delcared on top
						loader(layerName)
					}, // end success function
					error: function(){
						alert("failure");
					}
				});
				return false; // prevents refreshing page
			});	
		});
	</script>
</body>
</html>
