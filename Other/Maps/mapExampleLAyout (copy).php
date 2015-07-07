
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
	<div class="ui-layout-north">
	<!-- add extra utility buttons for the Themeswitcher tool -->
	<button onClick="removeUITheme()">Remove Theme</button> &nbsp; &nbsp;
	<button onClick="myLayout.resizeAll(); myLayout.sizeContent('center');">Resize Content</button>
</div>

<div class="ui-layout-west"> West </div>

<div class="ui-layout-east"> East </div>

<div class="ui-layout-south"> South </div>

<div class="ui-layout-center">
	<UL>
		<LI><a href="#tab_1"><SPAN>Tab 1</SPAN></a></LI>
		<LI><a href="#tab_2"><SPAN>Tab 2</SPAN></a></LI>
		<LI><a href="#tab_3"><SPAN>Tab 2</SPAN></a></LI>
	</UL>
	<div class="ui-layout-content"><!--  ui-widget-content -->
		<div id="tab_1">
			<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
			Vestibulum condimentum neque a velit laoreet dapibus. 
			Etiam eleifend tempus pharetra. Aliquam vel ante mauris, eget aliquam sapien. 
			Aenean euismod vulputate quam, eget vehicula lectus placerat eu. 
			Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. 
			Curabitur et ipsum orci, at fermentum metus. Etiam volutpat metus sit amet sapien tincidunt 
			non fermentum velit aliquet. Pellentesque malesuada accumsan mi a accumsan. 
			Nam commodo lectus non tellus rhoncus in facilisis metus iaculis. 
			Proin id sapien felis, sit amet pretium dui. Suspendisse purus erat, blandit ut mollis elementum, 
			bibendum a leo. Curabitur pulvinar arcu quis orci ultricies vestibulum. 
			Cras convallis nisi eget tortor tristique gravida. Nam augue magna, dapibus in luctus ac, 
			tincidunt dapibus tellus. Donec massa metus, pretium sit amet pulvinar id, ultrices ac eros. 
			Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
			Maecenas placerat lacus nec tortor feugiat condimentum.</p>

			<p>Cras nec arcu sed nisi varius fermentum ut non nulla. Pellentesque ultricies condimentum nibh, 
			nec imperdiet felis laoreet sit amet. Aenean a molestie tortor. 
			Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
			Praesent enim magna, imperdiet adipiscing tempus nec, molestie id elit. Ut varius ante gravida 
			est dignissim sodales. Nulla consectetur nibh eget metus sodales vulputate. 
			Mauris lacinia risus nec ipsum sodales elementum. Nunc non tortor turpis. 
			Vestibulum a euismod ligula.</p>

			<p>Nam non hendrerit augue. Nunc sit amet est lectus. Morbi non nisl eget dolor rutrum ullamcorper. 
			Sed dictum commodo elit sed rutrum. Nunc eu massa nulla, at gravida dolor. Aenean at interdum nisi. 
			Integer consequat malesuada urna quis dignissim. Duis luctus porta ullamcorper. 
			Aliquam tortor nunc, porta vel vestibulum at, egestas id mi. 
			In quis arcu in felis laoreet varius a et ligula. 
			Sed in magna a orci posuere ullamcorper ultrices ut ante. Suspendisse velit enim, venenatis et 
			pharetra sed, mollis ut dui. Donec erat eros, dignissim ac ultrices ac, hendrerit a elit.</p>

			<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
			Vestibulum condimentum neque a velit laoreet dapibus. 
			Etiam eleifend tempus pharetra. Aliquam vel ante mauris, eget aliquam sapien. 
			Aenean euismod vulputate quam, eget vehicula lectus placerat eu. 
			Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. 
			Curabitur et ipsum orci, at fermentum metus. Etiam volutpat metus sit amet sapien tincidunt 
			non fermentum velit aliquet. Pellentesque malesuada accumsan mi a accumsan. 
			Nam commodo lectus non tellus rhoncus in facilisis metus iaculis. 
			Proin id sapien felis, sit amet pretium dui. Suspendisse purus erat, blandit ut mollis elementum, 
			bibendum a leo. Curabitur pulvinar arcu quis orci ultricies vestibulum. 
			Cras convallis nisi eget tortor tristique gravida. Nam augue magna, dapibus in luctus ac, 
			tincidunt dapibus tellus. Donec massa metus, pretium sit amet pulvinar id, ultrices ac eros. 
			Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
			Maecenas placerat lacus nec tortor feugiat condimentum.</p>

			<p>Cras nec arcu sed nisi varius fermentum ut non nulla. Pellentesque ultricies condimentum nibh, 
			nec imperdiet felis laoreet sit amet. Aenean a molestie tortor. 
			Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
			Praesent enim magna, imperdiet adipiscing tempus nec, molestie id elit. Ut varius ante gravida 
			est dignissim sodales. Nulla consectetur nibh eget metus sodales vulputate. 
			Mauris lacinia risus nec ipsum sodales elementum. Nunc non tortor turpis. 
			Vestibulum a euismod ligula.</p>
		</div>
		<div id="tab_2">
			<p>Nam non hendrerit augue. Nunc sit amet est lectus. Morbi non nisl eget dolor rutrum ullamcorper. 
			Sed dictum commodo elit sed rutrum. Nunc eu massa nulla, at gravida dolor. Aenean at interdum nisi. 
			Integer consequat malesuada urna quis dignissim. Duis luctus porta ullamcorper. 
			Aliquam tortor nunc, porta vel vestibulum at, egestas id mi. 
			In quis arcu in felis laoreet varius a et ligula. 
			Sed in magna a orci posuere ullamcorper ultrices ut ante. Suspendisse velit enim, venenatis et 
			pharetra sed, mollis ut dui. Donec erat eros, dignissim ac ultrices ac, hendrerit a elit.</p>
		</div>
		<div id="tab_3">
			<p>Cras nec arcu sed nisi varius fermentum ut non nulla. Pellentesque ultricies condimentum nibh, 
			nec imperdiet felis laoreet sit amet. Aenean a molestie tortor. 
			Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
			Praesent enim magna, imperdiet adipiscing tempus nec, molestie id elit. Ut varius ante gravida 
			est dignissim sodales. Nulla consectetur nibh eget metus sodales vulputate. 
			Mauris lacinia risus nec ipsum sodales elementum. Nunc non tortor turpis. 
			Vestibulum a euismod ligula.</p>
		</div>
	</div>
</div>
</body>
</html>
