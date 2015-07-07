<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
	
    <title>SB Admin - Bootstrap Admin Template</title>
	
	<style>
	</style>


    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/sb-admin.css" rel="stylesheet">

    <!-- Morris Charts CSS -->
    <link href="css/plugins/morris.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">

	<!-- Load Openlayers - openlayers 2.13 cause issue with geoserver-->
	<script src="OpenLayers-2.12/OpenLayers.min.js"></script>
	

	
	<!-- OpenLayers -->
	<script  type="text/javascript">
		var map;
		var osm
		<!-- function to create the map layer -->
		function init(){
			
			map = new OpenLayers.Map({
			div: "map"
			});
			var something = 'esoteriko:clusternodes_';
			//alert(something);
			osm = new OpenLayers.Layer.OSM();	
			wms_layer_larisa =  new OpenLayers.Layer.WMS( "Larisa","http://192.168.2.6:8080/geoserver/gwc/service/wms",  //http://192.168.2.6:8080/geoserver/wms
				{
					"layers": 'esoteriko:clusternodes_',
					"format":  "image/png",
					"transparent": true,
					"version": "1.1.1",
					tiled: true,
					
				},
				{
					format: "image/png",
					displayOutsideMaxExtent: false,
					projection: new OpenLayers.Projection("EPSG:900913"),
				}
			);
			
			map.addLayers([wms_layer_larisa,osm]);
			
		
			 
			
			// SET CORRECT PROJECTION FOR LAYERS - CENTER AND ZOOM LEVEL (7)
			var lonLat = new OpenLayers.LonLat(22.421743,39.626646).transform(new  OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
			map.setCenter (lonLat, 13);

			map.addControl(new OpenLayers.Control.LayerSwitcher());
		};
 
		function loader(layerName){
			//alert(layerName);
			var indexLayer = layerName.indexOf(":");
			var layerName = layerName.substring(indexLayer+1);
			var layerName = $.trim(layerName); // trip whitespaces
			//alert(layerName);
			var workspace = 'esoteriko:';
			var layerName2 = String('esoteriko:'.concat(layerName));
			//alert(layerName2);
			
		// ADD THE LAYER OPENLAYERS
			wms_layer_larisa2 =  new OpenLayers.Layer.WMS(layerName,"http://192.168.2.6:8080/geoserver/gwc/service/wms",  //http://192.168.2.6:8080/geoserver/wms
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
                <a class="navbar-brand" href="index.html">SB Admin</a>
            </div>
            <!-- Top Menu Items -->
            <ul class="nav navbar-right top-nav">
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="fa fa-envelope"></i> <b class="caret"></b></a>
                    <ul class="dropdown-menu message-dropdown">
                        <li class="message-preview">
                            <a href="#">
                                <div class="media">
                                    <span class="pull-left">
                                        <img class="media-object" src="http://placehold.it/50x50" alt="">
                                    </span>
                                    <div class="media-body">
                                        <h5 class="media-heading"><strong>MarCO</strong>
                                        </h5>
                                        <p class="small text-muted"><i class="fa fa-clock-o"></i> Yesterday at 4:32 PM</p>
                                        <p>Lorem ipsum dolor sit amet, consectetur...</p>
                                    </div>
                                </div>
                            </a>
                        </li>
                        <li class="message-preview">
                            <a href="#">
                                <div class="media">
                                    <span class="pull-left">
                                        <img class="media-object" src="http://placehold.it/50x50" alt="">
                                    </span>
                                    <div class="media-body">
                                        <h5 class="media-heading"><strong>MarCO</strong>
                                        </h5>
                                        <p class="small text-muted"><i class="fa fa-clock-o"></i> Yesterday at 4:32 PM</p>
                                        <p>Lorem ipsum dolor sit amet, consectetur...</p>
                                    </div>
                                </div>
                            </a>
                        </li>
                        <li class="message-preview">
                            <a href="#">
                                <div class="media">
                                    <span class="pull-left">
                                        <img class="media-object" src="http://placehold.it/50x50" alt="">
                                    </span>
                                    <div class="media-body">
                                        <h5 class="media-heading"><strong>MarCO</strong>
                                        </h5>
                                        <p class="small text-muted"><i class="fa fa-clock-o"></i> Yesterday at 4:32 PM</p>
                                        <p>Lorem ipsum dolor sit amet, consectetur...</p>
                                    </div>
                                </div>
                            </a>
                        </li>
                        <li class="message-footer">
                            <a href="#">Read All New Messages</a>
                        </li>
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="fa fa-bell"></i> <b class="caret"></b></a>
                    <ul class="dropdown-menu alert-dropdown">
                        <li>
                            <a href="#">Alert Name <span class="label label-default">Alert Badge</span></a>
                        </li>
                        <li>
                            <a href="#">Alert Name <span class="label label-primary">Alert Badge</span></a>
                        </li>
                        <li>
                            <a href="#">Alert Name <span class="label label-success">Alert Badge</span></a>
                        </li>
                        <li>
                            <a href="#">Alert Name <span class="label label-info">Alert Badge</span></a>
                        </li>
                        <li>
                            <a href="#">Alert Name <span class="label label-warning">Alert Badge</span></a>
                        </li>
                        <li>
                            <a href="#">Alert Name <span class="label label-danger">Alert Badge</span></a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">View All</a>
                        </li>
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="fa fa-user"></i> MarCO <b class="caret"></b></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="#"><i class="fa fa-fw fa-user"></i> Profile</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-fw fa-envelope"></i> Inbox</a>
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
									<!--<input type="text" class="form-control" id="inputShp" placeholder="Shape File Path" data-toggle="tooltip" title="Shape file path"> -->
								
									<!-- DROPDOWN MENU LISTING ALL SHAPE FILES -->
									
									<div class="input-group">
										
										
										<div class="input-group-btn">
											<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
												Select Shape File
												<span class="caret"></span>
											</button>
											
										
			
											<ul id="dropdown-menu-id" class="dropdown-menu" role="menu">
												
												<?php foreach(glob("RunPythonThroughPHP/marCO/src/outputDistributionStuff/*.shp") as $filename){
												// GET INDEX
												$pos = strpos($filename, 'outputDistributionStuff/');
												// GET SUBSTRING WITH SHAPE NAME
												$rest = substr($filename, $pos+24);
												echo "<li class='demolist'><a href=>".$rest."</a></li>";   
												}
												?>
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
	
	<!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

	 <!-- SHAPE LOADER -->
	<script>	
		$(document).ready(function(){
			$('.demolist').on('click', function(){
				var shapeName =  $(this).find("a").text(); // GET THE VALUE OF DROPDOWN MENU AND PLACE IT TO TEXTFIELD
				var wholePath = 'RunPythonThroughPHP/marCO/src/outputDistributionStuff/'+shapeName;
				$('#inputShp').val(wholePath);
				 $("#dropdown-menu-id").dropdown("toggle"); // CLOSE THE DROPDOWN MENU AFTER SELECTION
				 
				 // MAKE AJAX REQUEST TO PASS SHAPE FILE
				 $.ajax({
					type: "POST",
					url: 'RunPythonThroughPHP/requests/shapeLoader.php',
					data: {shapeName:shapeName }, // PASS THE NAME OF THE SHAPE FILE - WHICH WILL BE THE NAME OF THE TABLE
					success: function(layerName){
						//alert(layerName);
						var layerName =  'esoteriko:'.concat(layerName);
						//alert(layerName);
						// LOADS THE NEWLY GENERATED LAYER
						loader(layerName)
						
					}, // end success function
					error: function(){
						alert("failure");
					}
				});
				
				return false; // PREVENTS REFRESING PAGE
				
			});
			
			
			
		});
	</script>
	
	
	

</body>

</html>
