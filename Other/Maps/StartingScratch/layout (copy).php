<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
		<!-- LOAD LIBRARIES -->
		<!-- GoogleMaps API key -->
        <script type="text/javascript"  src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDGRfizaRoe6AXpoOPz5HRTvRmY5yFSaAE&language=el&sensor=false"></script>
        <!-- LOAD OpenLayers library -->
        <script src="OpenLayers-2.12/OpenLayers.min.js"></script>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"> </script> <!-- Jquery library-->
		<script src="proj4js/lib/proj4js-compressed.js"></script> <!-- Proj4js library for projection transformation-->
		
		
		<!-- ADDITIONS I -->
		<meta charset="utf-8">
		<title>Esoteriko</title>
		<!-- LOAD JQuery library -->
		<script src="//code.jquery.com/jquery-1.10.2.js"></script>
		<!-- LOAD JQuery UI library -->
		<link rel="stylesheet" type="text/css" href="jquery-ui-1.11.4.custom/jquery-ui.css">
		<script src="jquery-ui-1.11.4.custom/jquery-ui.min.js"></script> 
		<!-- LOAD JQuery Layout library -->
		<script src="JQueryLayout1.4/jquery.layout.js"></script> 
		<!-- <link rel="stylesheet" href="/resources/demos/style.css"> -->
		<script>
			$(function() {
				$( "#tabs" ).tabs();
			});
		</script>
		
		<!-- ADDITIONS II LAYOUT -->
		<script>
			<script type="text/javascript">	
				$(document).ready(function () {
					$('body').layout({ applyDemoStyles: true });
				});
		</script>

		<!--<link type="text/css" href="Css/style.css" rel="Stylesheet"></script> -->
		<script type="text/javascript" src="JQueryLayout1.4/layout.js"></script>
		
		
		<!-- ADDITIONS III WIJMO -->
		
		<script type="text/javascript" src="Form/form.js"></script>
		
		
		
		
		
		<!-- DEFINE STYLES -->
		<style>
		.openlayers-map img{ margin:0px }	
		.toolbar-label,.x-btn-text,.x-boundlist-item,.x-boundlist-list-ct,.x-form-text{
                font-size: 12pt !important;
            }
            .x-btn-text{
                height: 18px !important;
            }
            .borderbtn{
                border-style:solid !important;
                border-width:1px !important;
                -moz-border-radius: 5px !important;
                border-radius: 5px !important;
            }
            .x-panel-body{
                background-color : #BFD9F2!important;
            }
            #panel.td{
                text-align: center !important;
            }
		</style>
		
				<script defer="defer" type="text/javascript">
		<!-- DEFINE PROXY.CGI URL -->
		OpenLayers.ProxyHost = "http://localhost/cgi-bin/proxy.cgi?url="; // path from cgi-bin defined path: usr->lib->cgi-bin
		//OpenLayers.ProxyHost = "http://localhost/cgi-bin/proxy.cgi?url=";

		
		<!-- DEFINE GLOBAL VARIABLES -->
		var map,wms,satellite,physical,imageslayer,control,clickControl;
		<!-- DEFINE PROJECTION DEFINITION --> CHECK THIS SITE FOR INFO  http://www.peterrobins.co.uk/it/olchangingprojection.html
		Proj4js.defs["EPSG:2100"] = "+proj=tmerc +lat_0=0 +lon_0=24 +k=0.9996 +x_0=500000 +y_0=0 +ellps=GRS80 +towgs84=-199.87,74.79,246.62,0,0,0,0 +units=m +no_defs";
		
		<!-- DEFINE FUNCTION INIT -->
		function init(){
			
			//SET ZOOM PARAMETER FOR LOADING FEATURES
			map = new OpenLayers.Map('map',{
                isBaseLayer: true,
                //controls: []
			}); // define map 
			
			wms = new OpenLayers.Layer.WMS( "OpenLayers WMS","http://vmap0.tiles.osgeo.org/wms/vmap0", 
				{
				layers: 'basic'
				},
				{
				isBaseLayer: true
				}); // define map layer
			
			

           satellite = new OpenLayers.Layer.Google(
                "Satellite View",
                {type: google.maps.MapTypeId.HYBRID,
                numZoomLevels: 23,
				MAX_ZOOM_LEVEL: 22}
                
            );
            
            physical = new OpenLayers.Layer.Google(
                "Physical View",
                { type: google.maps.MapTypeId.PHYSICAL,
                numZoomLevels: 23,
				MAX_ZOOM_LEVEL: 22}
                
            );

			// add layers
			map.addLayers([satellite,physical]); // first you put the layer with the points
			var lonLat = new OpenLayers.LonLat(22.191969,38.784336).transform(new  OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
			map.setCenter (lonLat, 6);

			<!-- ADD CONTROLS -->
			map.addControl(new OpenLayers.Control.LayerSwitcher());
			map.addControl(new OpenLayers.Control.Navigation({'zoomBoxEnabled':false})); 
			//map.addControl(new OpenLayers.Control.PanZoomBar());
			map.addControl(new OpenLayers.Control.ArgParser());
			map.addControl(new OpenLayers.Control.Attribution());
			//map.addControl(new OpenLayers.Control.ScaleLine());
			
			
		}
			

		
		</script>			
	</head>

</head>
<!-- START BODY-->
	<body onload="init()">
		<!-- CHANGE STATUS -->
		
		
			
<div class="ui-layout-center">
	<div id="tabs">
			<ul>
				<li><a href="#tabs-1">Map</a></li>
				<li><a href="#tabs-2">Excel</a></li>
			</ul>
		<div id="tabs-1">
			<div id="map" style="width:1200px;height:500px"></div>
		</div>
		<div id="tabs-2">
			<!--<div id="ss" style="width: 600; height: 400;"></div>-->
		</div>
		</div>
</div>
<div class="ui-layout-north">North</div>
<div class="ui-layout-east">East</div>

</body>
</html>
