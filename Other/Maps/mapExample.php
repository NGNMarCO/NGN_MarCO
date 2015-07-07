
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">

<head>
	
	<title>jQuery UI | OpenLayers</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta author="dkar"></meta>
	<meta description="OpenLayers JQueryUI"></meta>
	<meta keywords="openlayers jquery"></meta>
	<meta name="language" content="en"></meta>
		
	<!-- Google Maps API Key -->
	<script type="text/javascript"  src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDGRfizaRoe6AXpoOPz5HRTvRmY5yFSaAE&language=el&sensor=false"></script>
	<!-- OpenLayers -->
	<script src="JsLib/OpenLayers.min.js"></script>
	
	<!-- jQuery-UI, qTip & jQuery-UI.Layout -->

	<script type="text/javascript" src="JsLib/jquery-1.3.2.min.js"></script>
	<script type="text/javascript" src="JsLib/jquery-ui-1.7.2.custom.min.js"></script>
	<script type="text/javascript" src="JsLib/jquery.qtip-1.0.0-rc3.min.js"></script>
	<script type="text/javascript" src="JsLib/jquery.layout.js"></script>
	
	
	<!-- Added from panels source code -->
	 <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">

	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
	<link rel="stylesheet" href="/resources/demos/style.css">
	
	 
	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
	
	
	
	
	<!-- Javascript Css personalizzati-->
	<link type="text/css" href="Css/style.css" rel="Stylesheet"></script>
	<script type="text/javascript" src="layout.js"></script>
	<script type="text/javascript" src="map.js"></script>
  
	<script>
		$(function() {
			$( "#tabs" ).tabs();
		});
	</script>
  
  
</head>
<body onload="initMap()">
	<!-- header -->
	<div class="ui-layout-north" id="header">
		<!-- toolbar superiore -->
		<div class="fg-toolbar ui-widget-header ui-corner-all ui-helper-clearfix">
			
			<div class="fg-buttonset ui-helper-clearfix">
				<a href="#" class="fg-button ui-state-default fg-button-icon-solo ui-corner-all" title="Full extent" onclick="map.zoomToExtent(bounds);"><span class="ui-icon fullextent"></span> Full Extent</a>
			</div>
			<div class="fg-buttonset fg-buttonset-single">
				<a href="#" class="fg-button ui-state-default fg-button-icon-solo" title="Zoom in" name="zoomin" onclick="toggleControl(this)";"><span class="ui-icon zoom_in"></span> Zoom in</a>
				<a href="#" class="fg-button ui-state-default fg-button-icon-solo ui-state-active" title="Pan" name="pan"	onclick="toggleControl(this)";"><span class="ui-icon pan"></span> Pan</a>
				<a href="#" class="fg-button ui-state-default fg-button-icon-solo" title="Zoom out" name="zoomout" onclick="toggleControl(this)";"><span class="ui-icon zoom_out"></span> Zoom out</a>
				<a href="#" class="fg-button ui-state-default fg-button-icon-solo" title="Misura lunghezza" name="line" onclick="toggleControl(this)";"><span class="ui-icon ruler"></span> Misura lunghezza</a>
				<a href="#" class="fg-button ui-state-default fg-button-icon-solo" title="Misura area" name="polygon" onclick="toggleControl(this)";"><span class="ui-icon ruler2"></span> Misura area</a>
			</div>
			<div class="fg-buttonset ui-helper-clearfix">
				<div id="btnPrev" class="fg-button ui-state-default fg-button-icon-solo" title="Vista precedente"></div>
				<div id="btnNext" class="fg-button ui-state-default fg-button-icon-solo" title="Vista successiva"></div>
				<!-- <a href="#" class="fg-button ui-state-default fg-button-icon-solo" title="Vista precedente"><span id="prev" class="ui-icon prev"></span> Vista precedente</a> -->
				<!-- <a href="#" class="fg-button ui-state-default fg-button-icon-solo" title="Vista successiva"><span class="ui-icon next"></span> Vista successiva</a> -->
			</div>
		</div>
	</div>
	<!-- mappa -->
	<div class="ui-layout-center" id="map">
	</div>
	<!-- colonna di destra -->
	<div class="ui-layout-east" id="right">
			<div id="tabs">
				<ul>
				<li><a href="#tabs-1">Source Map</a></li>
				<li><a href="#tabs-2">Edges</a></li>

				</ul>
				<div id="tabs-1">
					<p>Proin elit arcu, rutrum commodo, vehicula tempus, commodo a, risus. Curabitur nec arcu. Donec sollicitudin mi sit amet mauris. Nam elementum quam ullamcorper ante. Etiam aliquet massa et lorem. Mauris dapibus lacus auctor risus. Aenean tempor ullamcorper leo. Vivamus sed magna quis ligula eleifend adipiscing. Duis orci. Aliquam sodales tortor vitae ipsum. Aliquam nulla. Duis aliquam molestie erat. Ut et mauris vel pede varius sollicitudin. Sed ut dolor nec orci tincidunt interdum. Phasellus ipsum. Nunc tristique tempus lectus.</p>
				</div>
				<div id="tabs-2">
					<p>Morbi tincidunt, dui sit amet facilisis feugiat, odio metus gravida ante, ut pharetra massa metus id nunc. Duis scelerisque molestie turpis. Sed fringilla, massa eget luctus malesuada, metus eros molestie lectus, ut tempus eros massa ut dolor. Aenean aliquet fringilla sem. Suspendisse sed ligula in ligula suscipit aliquam. Praesent in eros vestibulum mi adipiscing adipiscing. Morbi facilisis. Curabitur ornare consequat nunc. Aenean vel metus. Ut posuere viverra nulla. Aliquam erat volutpat. Pellentesque convallis. Maecenas feugiat, tellus pellentesque pretium posuere, felis lorem euismod felis, eu ornare leo nisi vel felis. Mauris consectetur tortor et purus.</p>
				</div>
			</div>
	</div>
	<!-- footer -->
	<div class="ui-layout-south"  id="footer">
			<!-- toolbar inferiore -->
			<div class="fg-toolbar ui-widget-header ui-corner-all ui-helper-clearfix">
				<div class="fg-buttonset fg-buttonset-single">
					<button class="fg-button ui-state-default ui-state-disabled">Coordinate:</button>
					<button class="fg-button ui-state-default ui-state-disabled"><span id="coord"></span></button>
				</div>
				<div class="fg-buttonset fg-buttonset-single">
					<button class="fg-button ui-state-default ui-state-disabled">Misure:</button>
					<button class="fg-button ui-state-default ui-state-disabled"><span id="output">...</span></button>
				</div>
			</div>
	</div>
</body>
</html>
