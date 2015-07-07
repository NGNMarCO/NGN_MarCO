<!DOCTYPE html>
    <html>

    <head>
        <link type="text/css" rel="stylesheet" href="../api/layout-master/source/stable/layout-default.css">
        <script type="text/javascript" src="../api/layout-master/source/jquery/jquery.js"></script>
        <script type="text/javascript" src="../api/layout-master/source/stable/jquery.layout.js"></script>
        <script type="text/javascript" src="../../OpenLayers/v2.0/OpenLayers.js"></script>
        <style type="text/css">
            .ui-layout-toggler-west,
            .ui-layout-toggler-south {
                border: 0;
            }
            .ui-layout-toggler-west div {
                width: 8px;
                height: 35px;
            }
            .ui-layout-toggler-south div {
                width: 35px;
                height: 8px;
                float: left;
            }
        </style>
        <script type="text/javascript">
            function init() {
                var options = {
                    projection: new OpenLayers.Projection("EPSG:32643"),
                    units: "m",
                    numZoomLevels: 10,
                    maxExtent: new OpenLayers.Bounds(401623.280957, 1282418.1261, 888858.311664, 2044579.876058)
                };
                var map = new OpenLayers.Map("map", options)
                osm  = new OpenLayers.Layer.OSM("Open Street Map");
                map.addLayer(osm);
                map.zoomToMaxExtent();
            };


        </script>
    </head>

    <body>
        <div class="ui-layout-center" id="map">
         </div>
        <div class="ui-layout-north"> </div>
        <div class="ui-layout-south"> </div>
        <div class="ui-layout-east"> </div>
        <div class="ui-layout-west"> </div>
    </body>

</html>
