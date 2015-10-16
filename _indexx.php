<!DOCTYPE html>
<!-- 3rd party tools used: BootstrapCSS framework
Short Description: _indexx.php contains the Input form of the application. 
The user can either type the values or select the "Default Values" button to 
autofill the values. When pressig "RUN" button the Python algorithm (of Thanasis)
is executed. 
Current state: It might be that part of the Python code is commented thus when selecting RUN
it only executes the uncommented part (in this case the clustering part). 
Also, by pressing "Default values" some of the text fields are not populated. These values
are still hardcoded inside the Python file (has to change).
Improvements: 1) use a BootstrapCSS "progress bar" in order to show the steps of code execution
2) when clicking "RUN" make a validation of the inputs and pass them into a database table (postgreSQL)-->

<html lang="en">
<head>
    <title>MarCO</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
	<!-- Load Frameworks-->
    <!-- Bootstrap Core CSS -->
    <link href="Libs/BootStrapCSS/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="Libs/BootStrapCSS/css/sb-admin.css" rel="stylesheet">
    <!-- Custom Fonts -->
    <link href="Libs/BootStrapCSS/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <!-- my CSS -->
    <link href="Libs/BootStrapCSS/css/myCss.css" rel="stylesheet">
  
</head> 

<body>
    <div id="wrapper">
        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
            </div> <!-- end navbar-header -->
            <!-- Top Menu Items: Not used for anything right now -->
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
					<li class="active">
                        <a href="_indexx.php"><i class="fa fa-fw fa-edit"></i> Input Form</a>
                    </li>
                    <li>
                        <a href="_spreadsheet.html"><i class="fa fa-fw fa-table"></i> Excel</a>
                    </li>
                    
                    <li>
                        <a href="_map.php"><i class="fa fa-fw fa-map-marker"></i> Map</a>
                    </li>
                </ul>
            </div> <!-- /.navbar-collapse -->
        </nav>
		<!-- Create the Form -->
        <div id="page-wrapper">
                <form>
                <!-- Page Heading -->
                <div class="row">
                    <div class="col-lg-12">	
                        <ol class="breadcrumb">
                            <li>
                                <i class="fa fa-dashboard active"></i>  <a href="_indexx.html">Input Form</a>
                            </li>
                 
                        </ol>	
                    </div> <!-- col-lg-12 -->
                </div> <!-- /.row -->
				<div class="row">
					<div class="col-lg-6">   <!-- /.PROBLEM WHERE DOES IT CLOSE -->
						<div class="panel panel-primary">
							<div class="panel-heading">
								<h3 class="panel-title"><i class="fa fa-table"></i> General</h3>
							</div>  <!-- /.panel-heading -->
							<div class="panel-body"  style="height:100%">
									
									<div class="form-group">
										<input type="text" class="form-control" id="inputName" placeholder="Scenario Name" data-toggle="tooltip" title="Name of the run">
									</div>
									<div class="form-group">
										<input type="text" class="form-control" id="inputDescription" placeholder="Scenario Description" data-toggle="tooltip" title="Description">
									</div>	
							</div>  <!-- /.panel-body -->
                        </div> <!-- /.panel-primary -->
                    </div>  <!-- /.col-lg-6 -->
					<div class="col-lg-6">
						<div class="panel panel-success">
							<div class="panel-heading">
								<h3 class="panel-title"><i class="fa fa-table"></i> Clustering</h3>
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
												<?php foreach(glob("Code/python/inputShp/larissa_subset/*.shp") as $filename){
													// GET INDEX
													$pos = strpos($filename, 'larissa_subset/');
													// GET SUBSTRING WITH SHAPE NAME
													$rest = substr($filename, $pos+15);
													echo "<li class='demolist'><a href='#'>".$rest."</a></li>";   
												}?>
											</ul>	
										</div> <!-- /btn-group -->
										<input type="text" class="form-control" id="inputShp" placeholder="Shape File Path" data-toggle="tooltip" title="Shape file path">		
									</div> <!-- /input-group -->
								</div>
                                
                                
                                <!-- old id for clusters: inputNumCab -->
 
                                <div class="row">
										<div class="col-lg-4">
											<div class="form-group">
												<input type="text" class="form-control" id="inputTotalPopulation" placeholder="Population" data-toggle="tooltip" title="Total Population of Area">
											</div>
										</div>
										<div class="col-lg-4">
											<div class="form-group">
												<input type="text" class="form-control" id="inputKVcapacity" placeholder="Capacity of KV" data-toggle="tooltip" title="Number of Users a KV can Host">
											</div>
										</div>
                                        <div class="col-lg-4">
											<div class="form-group">
												<input type="text" class="form-control" id="inputNumClusters" placeholder="Number Of Cabinets" readonly="readonly" data-toggle="tooltip" title="Calculated Number of Clusters">
											</div>
										</div>
                                </div>  <!-- /.row -->
							</div> <!-- /.panel body -->
						</div> <!-- /.panel success -->
					</div> <!-- /.col-lg-6 -->	
				</div> <!-- /.row -->
                <div class="row">
                    
					<div class="col-lg-6">
                        <div class="panel panel-success">
							<div class="panel-heading">
                                    <h3 class="panel-title"><i class="fa fa-table"></i> Distribution Network - Cable & Subducts Granularities</h3>
                            </div> <!-- /.panel-heading-->
                            <div class="panel-body"  style="height:100%">
                                    
									<div class="form-group">
                                        <div class="input-group">
                                            <div class="input-group-btn">
                                                <!--  button to activate modal -->
                                                <a href="#" id= 'dist_granularities_help' class="btn btn-success btn-mg" data-toggle="modal" data-target="#myModal" title="Help" ><span class="glyphicon glyphicon-th-list"></span></a>  
                                            </div> <!-- /btn-group -->
                                            <input type="text" class="form-control" id="inputSubductsDist" placeholder="Cable & Subduct Granularity" data-toggle="tooltip" title="Cable & Subduct Granularity">		
                                        </div> <!-- /input-group -->	
									</div>

									<div class="form-group has-feedback">
										<input type="text" class="form-control" id="inputCostCableGranDist" placeholder="Costs for Cable & Subduct Granularity" data-toggle="tooltip" title="Costs for Cable & Subduct Granularity">
                                        <i class="glyphicon glyphicon-euro form-control-feedback"></i> <!-- euro icon -->
                                    </div>
                                    
                                    <div class="form-group has-feedback">
										<input type="text" class="form-control" id="inputcostKVDist" placeholder="KV Cost" data-toggle="tooltip" title="Cost of the KV in Euro">
                                        <i class="glyphicon glyphicon-euro form-control-feedback"></i> <!-- euro icon -->
                                    </div>
										
									<div class="form-group">
										<input type="text" class="form-control" id="inputPercentageOfCoverageDist" placeholder="Total Coverage 100%" value="100" readonly="readonly" data-toggle="tooltip" title="Percentage of Area to Cover">
									</div>	 
                            </div>	 <!-- /.panel-body -->
						</div>	 <!-- /.panel-success-->				    
					</div>   <!-- /.col-lg-6-->
                    
					<div class="col-lg-6">
                        <div class="panel panel-success">
							<div class="panel-heading">
								<h3 class="panel-title"><i class="fa fa-table"></i> Distribution Network - Manhole Strategy </h3>
							</div>
							<div class="panel-body"  style="height:100%">
									
									<div class="form-group has-feedback">
										<input type="text" class="form-control" id="inputManHoleCostDist" placeholder="Manhole Cost" data-toggle="tooltip" title="Cost of one Manhole">
                                        <i class="glyphicon glyphicon-euro form-control-feedback"></i> <!-- euro icon -->
									</div>
									
									<div class="row">
										<div class="col-lg-6">
											<div class="form-group">
												<input type="text" class="form-control" id="inputminDistDist" placeholder="Minimum Distance" data-toggle="tooltip" title="Minimum Distance to Place Manhole">
											</div>
										</div> <!-- /.col-lg-6-->
										<div class="col-lg-6">
											<div class="form-group">
												<input type="text" class="form-control" id="inputmaxDistDist" placeholder="Maximum Distance" data-toggle="tooltip" title="Maximum Distance to Place Manhole">
											</div>
										</div> <!-- /.col-lg-6-->
									</div> <!-- /.eow-->
									
									<div class="row">
										<div class="col-lg-4">
											<div class="form-group">
												<label class="btn btn-primary active">
													<input type="checkbox" value="news" class="cbManholeDist" id="inputManholeStrDist1" data-toggle="tooltip" title="Manhole in 1 way junction"> 1-Way
												</label>
											</div>
										</div> <!-- /.col-lg-4-->
										<div class="col-lg-4">
											<div class="form-group">
												<label class="btn btn-primary active">
													<input type="checkbox" value="news" class="cbManholeDist" id="inputManholeStrDist2" data-toggle="tooltip" title="Manhole in two ways junction"> 2-Way
												</label>
											</div>
										</div> <!-- /.col-lg-4-->
										<div class="col-lg-4">
											<div class="form-group">
												<label class="btn btn-primary active">
													<input type="checkbox" value="news" class="cbManholeDist" id="inputManholeStrDist3" data-toggle="tooltip" title="Manhole in three ways junction"> 3-Way
												</label>
											</div>
										</div> <!-- /.col-lg-4-->
									</div>	<!-- /.row-->
									<div class="row">
										<div class="col-lg-4">
											<div class="form-group">
												<div class="dropdown">
													<button id="btn_manholeNewCosts" class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Average<span class="caret"></span></button>
														<ul id="ul_manholeNewCosts" class="dropdown-menu">
															<li><a href = "javascript:return false;">Cheap</a></li>
															<li><a href = "javascript:return false;">Average</a></li>
															<li><a href = "javascript:return false;">Expensive</a></li>
														</ul>
												</div>
											</div>
										</div> <!-- /.col-lg-4-->
										<!-- Checkboxes for LC and HC (low cost and high cost for manhole)  -->
										<div class="col-lg-4">
											<div class="form-group">
												<div class="dropdown">
													<button id="btn_inputManhole_cost2_Dist" class="btn btn-primary dropdown-toggle hidden" type="button" data-toggle="dropdown">LC/HC<span class="caret"></span></button>
														<ul id="ul_inputManhole_cost2_Dist" class="dropdown-menu">
															<li><a href = "javascript:return false;">Low Cost</a></li>
															<li><a href = "javascript:return false;">High Cost</a></li>
														</ul>
												</div> <!-- /.dropdown-->
											</div> <!-- /.form group-->
										</div> <!-- /.col-lg-4-->
										
										<div class="col-lg-4">
											<div class="form-group">
												<div class="dropdown">
													<button id="btn_inputManhole_cost3_Dist" class="btn btn-primary dropdown-toggle hidden" type="button" data-toggle="dropdown">LC/HC<span class="caret"></span></button>
														<ul id="ul_inputManhole_cost3_Dist" class="dropdown-menu">
															<li><a href = "javascript:return false;">Low Cost</a></li>
															<li><a href = "javascript:return false;">High Cost</a></li>
														</ul>
												</div> <!-- /.dropdown-->
											</div> <!-- /.form group-->
										</div> <!-- /.col-lg-4-->
                                    
									</div> <!-- /.row-->
							</div> <!-- /panel body-->
						</div>	<!-- /.panel success-->				    
					</div> <!-- /.col-lg-6-->
				</div>   <!-- /.row-->      
                <div class="row">
					<div class="col-lg-6">
                        <div class="panel panel-info">
							<div class="panel-heading">
									<h3 class="panel-title"><i class="fa fa-table"></i> Feeder Network - Cable & Subducts Granularities</h3>
                            </div> <!-- /.panel heading -->
                            <div class="panel-body"  style="height:100%">
                                <div class="form-group">
										<input type="text" class="form-control" id="inputSubductsFeeder" placeholder="Cable & Subduct Granularity" data-toggle="tooltip" title="Cable & Subduct Granularity">
									</div>
                                <div class="form-group has-feedback">
										<input type="text" class="form-control" id="inputCostCableGranFeeder" placeholder="Costs for Cable & Subduct Granularity" data-toggle="tooltip" title="Costs for Cable & Subduct Granularity">
                                        <i class="glyphicon glyphicon-euro glyphicon-euro form-control-feedback"></i> <!-- euro icon -->
									</div>
                                <div class="form-group has-feedback">
										<input type="text" class="form-control" id="inputcostCO" placeholder="Central Office Cost" data-toggle="tooltip" title="Cost of the Central Office in Euro">
                                        <i class="glyphicon glyphicon-euro glyphicon-euro form-control-feedback"></i> <!-- euro icon -->
                                    </div>
                            </div>	 <!-- /.panel body -->
						</div> <!-- /.panel -->					    
					</div>   <!-- /.col-lg-6 -->
					<div class="col-lg-6">
                        <div class="panel panel-info">
							<div class="panel-heading">
								<h3 class="panel-title"><i class="fa fa-table"></i> Feeder Network - Manhole Strategy</h3>
							</div>	<!-- /.panel heading -->
							<div class="panel-body"  style="height:100%">
									<div class="form-group has-feedback">
										<input type="text" class="form-control" id="inputManHoleCostFeeder" placeholder="Manhole Cost" data-toggle="tooltip" title="Cost of one Manhole" >
                                        <i class="glyphicon glyphicon-euro glyphicon-euro form-control-feedback"></i> <!-- euro icon -->
                                    </div> <!-- /.formgroup -->
									
									<div class="row">
										<div class="col-lg-6">
											<div class="form-group">
												<input type="text" class="form-control" id="inputminDistFeeder" placeholder="Minimum Distance" data-toggle="tooltip" title="Minimum Distance to Place Manhole">
											</div>
										</div>
										<div class="col-lg-6">
											<div class="form-group">
												<input type="text" class="form-control" id="inputmaxDistFeeder" placeholder="Maximum Distance" data-toggle="tooltip" title="Maximum Distance to Place Manhole">
											</div>
										</div>
									</div> <!-- /.row -->
									
									
									
									<div class="row">
										<div class="col-lg-4">
											<div class="form-group">
												<label class="btn btn-primary active">
													<input type="checkbox" value="news" class="cbManholeFeed" id="inputManholeStrFeed1" data-toggle="tooltip" title="Manhole in 1 way junction"> 1-Way
												</label>
											</div> <!-- form-group-->
										</div> <!-- /.col-lg-4 -->
										<div class="col-lg-4">
											<div class="form-group">
												<label class="btn btn-primary active">
													<input type="checkbox" value="news" class="cbManholeFeed" id="inputManholeStrFeed2" data-toggle="tooltip" title="Manhole in 2 ways junction"> 2-Way
												</label>
											</div>
										</div> <!-- /.col-lg-4 -->
										<div class="col-lg-4">
											<div class="form-group">
												<label class="btn btn-primary active">
													<input type="checkbox" value="news" class="cbManholeFeed" id="inputManholeStrFeed3" data-toggle="tooltip" title="Manhole in 3 ways junction"> 3-Way
												</label>
											</div>
										</div> <!-- /.col-lg-4 -->
									</div>	<!-- /.row -->
									
									<div class="row">
										<div class="col-lg-4">
											<div class="form-group">
												<div class="dropdown">
													<button id="btn_manholeNewCostsFeed" class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Average<span class="caret"></span></button>
														<ul id="ul_manholeNewCostsFeed" class="dropdown-menu">
															<li><a href = "javascript:return false;">Cheap</a></li>
															<li><a href = "javascript:return false;">Average</a></li>
															<li><a href = "javascript:return false;">Expensive</a></li>
														</ul>
												</div> <!-- /.dropdown -->
											</div> <!-- /.form group -->
										</div> <!-- /.col-lg-4 -->
										<!-- Checkboxes for LC and HC (low cost and high cost for manhole)  -->
										<div class="col-lg-4">
											<div class="form-group">
												<div class="dropdown">
													<button id="btn_inputManhole_cost2_Feed" class="btn btn-primary dropdown-toggle hidden" type="button" data-toggle="dropdown">LC/HC<span class="caret"></span></button>
														<ul id="ul_inputManhole_cost2_Feed" class="dropdown-menu">
															<li><a href = "javascript:return false;">Low Cost</a></li>
															<li><a href = "javascript:return false;">High Cost</a></li>
														</ul>
												</div>
											</div> <!-- /.form group -->
										</div> <!-- /.col-lg-4 -->  
										
										<div class="col-lg-4">
											<div class="form-group">
												<div class="dropdown">
													<button id="btn_inputManhole_cost3_Feed" class="btn btn-primary dropdown-toggle hidden" type="button" data-toggle="dropdown">LC/HC<span class="caret"></span></button>
														<ul id="ul_inputManhole_cost3_Feed" class="dropdown-menu">
															<li><a href = "javascript:return false;">Low Cost</a></li>
															<li><a href = "javascript:return false;">High Cost</a></li>
														</ul>
												</div>
											</div> <!-- /.form group -->
										</div> <!-- /.col-lg-4 -->
										
									</div> <!-- /.row -->
							</div> <!-- /.panel body -->	
						</div>	<!-- /.panel info -->				    
					</div> <!-- /.col-lg-6 -->
				</div>  <!-- /.row -->
				<div class="row">    
                     <div class="col-lg-6">
						<input id="btnExecute" type="button" class="btn btn-primary" value="Run" data-toggle="tooltip" title="Save data and execute algorithm">
						<input id="resetBtnId" type="reset" class="btn btn-default" value="Reset" data-toggle="tooltip" title="Delete all values from fields">
						<input id="btnDefaultVal" type="button" class="btn btn-default" value="Default Values" data-toggle="tooltip" title="Enter default values to the fields">	
					</div> <!-- /.col-lg-6 -->  
					<!-- Progress bar-->
					<div class="col-lg-6">
						<div class="alert alert-info">
							<div class="progress-label">Progress</div>
							<div class="progress">
								<div class="progress-bar progress-bar-success progress-bar-striped" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width:0%" > </div>
							</div> <!-- /.progress -->
						</div> <!-- /.alert-info -->
					</div>  <!-- /.col-lg-6 -->
                </div>  <!-- /.row -->            
                </form> <!-- /.form -->                 
        </div>	<!-- /#page-wrapper -->
    </div> <!-- /#wrapper -->
         
    
    
    
    
    <!-- MODALS-->
    <!-- Modals - This section contains all the modals -->
    <div class="modal fade" id="myModal" role="dialog">
        <div class="modal-dialog">
            <!-- Modal content-->
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <h4 class="modal-title">Modal Header</h4>
                </div> <!-- /. modal header -->
                <div class="modal-body">
                    <div id="leftColumnSvg">
                        <div class="form-group">
                            <input type="text" class="form-control" id="inputCableGranModal" placeholder="Cable Granulariy" data-toggle="tooltip" title="Cable Granulariy">
                        </div>
                        <div class="form-group" id="toggleTextModule">
                            Number of fibers inside the subduct (e.g. Figure has 4 fibers inside each subduct).
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" id="inputSubGranModal" placeholder="Subducts Granularity" data-toggle="tooltip" title="Subducts Granularity">
                        </div>
                        <div class="form-group" id="toggleTextModule_2">
                            Number of subducts inside the duct (e.g. Figure has 4 sybducts inside the duct).
                        </div>
                    </div>  <!-- /. leftColumnSvg -->
                 
                    <div id="rightColumnSvg">
                        <svg width="160" height="160">
                            <!-- duct -->
                            <circle cx="80" cy= "80" r="60" style="fill:#D3D3D3"/> 
                            <!-- subducts -->
                            <g id="subduct">
                                <circle cx="100" cy= "60" r="17" style="stroke:#FF4500; stroke-width: 4; fill:#000080"/>
                                <circle cx="60" cy= "100" r="17" style="stroke:#FF4500; stroke-width: 4; fill:#000080"/>
                                <circle cx="60" cy= "60" r="17" style="stroke:#FF4500; stroke-width: 4; fill:#000080"/>
                                <circle cx="100" cy= "100" r="17" style="stroke:#FF4500; stroke-width: 4; fill:#000080"/>
                            </g> <!-- /g -->
                            <!-- fibers in cable -->
                            <g id="duct">
                                <!--pano aristera -->
                                <circle cx="55" cy= "55" r="3" style="fill:#FF4500"/> <!--pano aristera -->
                                <circle cx="55" cy= "66" r="3" style="fill:#FF4500"/> <!--kato aristera -->
                                <circle cx="66" cy= "55" r="3" style="fill:#FF4500"/> <!--pano dexia -->
                                <circle cx="66" cy= "66" r="3" style="fill:#FF4500"/> <!--kato dexia -->
                                <!--pano dexia --> 
                                <circle cx="95" cy= "55" r="3" style="fill:#FF4500"/> <!--pano aristera -->
                                <circle cx="95" cy= "65" r="3" style="fill:#FF4500"/> <!--kato aristera -->
                                <circle cx="106" cy= "55" r="3" style="fill:#FF4500"/> <!--pano dexia -->
                                <circle cx="106" cy= "65" r="3" style="fill:#FF4500"/> <!--kato dexia -->
                                <!--kato aristera -->
                                <circle cx="55" cy= "96" r="3" style="fill:#FF4500"/> <!--pano aristera -->
                                <circle cx="66" cy= "96" r="3" style="fill:#FF4500"/> <!--pano dexia -->
                                <circle cx="55" cy= "106" r="3" style="fill:#FF4500"/> <!--kato aristera -->
                                <circle cx="66" cy= "106" r="3" style="fill:#FF4500"/> <!--kato dexia -->
                                <!--kato dexia -->
                                <circle cx="95" cy= "96" r="3" style="fill:#FF4500"/> <!--pano aristera -->
                                <circle cx="106" cy= "96" r="3" style="fill:#FF4500"/> <!--pano dexia -->
                                <circle cx="95" cy= "106" r="3" style="fill:#FF4500"/> <!--kato aristera -->
                                <circle cx="106" cy= "106" r="3" style="fill:#FF4500"/> <!--kato dexia -->
                            </g> <!-- /. g -->
                        </svg> <!-- /. svg -->
                    </div>
                    <button type="button" id="clearCssModal" class="btn btn-default">Clear</button>
                    <button type="button" id="passBtnModal"  class="btn btn-default" data-dismiss="modal" data-toggle="tooltip" title="Pass Data to Form">Pass</button>
                    <div class="modal-footer" style="display:none"></div>   
                </div>
                    </div> 
                </div>  <!-- end of modal-body -->
            </div> <!-- end of modal-content -->
        </div> <!-- end of modal-dialog -->
    </div> <!-- end of modal-fade -->
    
    
    
	
	<!-- Load libraries -->
    <!-- jQuery -->
    <script src="Libs/BootStrapCSS/js/jquery.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="Libs/BootStrapCSS/js/bootstrap.min.js"></script>	
    <!-- Load setManholeStrategy() function  -->	
	<script src="Code/jsFunctions/setManholeStrategy.js"></script>

	<!-- Tooltips for Input fields -->
	<script>
		$(document).ready(function(){
			$('[data-toggle="tooltip"]').tooltip();   
		});
	</script>
	
	
    
    <!-- MODAL - CHANGE COLOR OF SVGs ON TEXTFORM-->
    <script>
    $(document).ready(function(){
        // change color for subducts
        $("#inputSubGranModal").click(function() {
            $('#subduct').children("*").css('stroke','#FFFF00');
            $('#duct').children("*").css('fill','#FF4500');
            $( "#toggleTextModule" ).hide();    
        }); 
        // change color for duct
        $("#inputCableGranModal").click(function() {
            $('#duct').children("*").css('fill','#FFFF00');
            $('#subduct').children("*").css('stroke','#FF4500');
        }); 
        // reset colors and delete values
        $("#clearCssModal").click(function() {
            $('#duct').children("*").css('fill','#FF4500');
            $('#subduct').children("*").css('stroke','#FF4500');
            $( "#toggleTextModule" ).hide();
            $( "#toggleTextModule_2" ).hide();
            $('#inputCableGranModal').val("");
            $('#inputSubGranModal').val("");
        });
        // toggle help info
        $("#inputCableGranModal").click(function() {
            $( "#toggleTextModule" ).show();
            $( "#toggleTextModule_2" ).hide();
        });
        $("#inputSubGranModal").click(function() {
            $( "#toggleTextModule_2" ).show();
            $( "#toggleTextModule" ).hide();
        });
        // pass data from modal's text forms to main screen text forms
        $("#passBtnModal").click(function() {
            var CableGransModal = ($("#inputCableGranModal").val());
            var SubductsGransModal = ($("#inputSubGranModal").val());
            $("#inputSubductsDist").val("["+CableGransModal+"],[1]"+",["+SubductsGransModal+"],[1]");
        });
        
        
    
	});
    </script>
    
    
    
	<!-- SEND DATA FROM FORM TO PHP SCRIPT AND TO PYTHON PROGRAM TO RUN THE ALGORITHM -->
	<script>	
	$(document).ready(function(){
	 $("#btnExecute").click(function(){
		 
		// Execute the function ManholeStrategy() for calculating required parameters for manhole strategy for distribution network
		var manholeStrategyFunc = ManholeStrategy('inputManholeStrDist1','inputManholeStrDist2','inputManholeStrDist3','btn_inputManhole_cost2_Dist','btn_inputManhole_cost3_Dist','btn_manholeNewCosts');
		var manholeParamAsBinaryDist = manholeStrategyFunc[0]; // array with binar values
		var d = manholeStrategyFunc[1]; // manhole strategy
		
		// Execute the function ManholeStrategy() for calculating required parameters for manhole strategy for feeder network
		var manholeStrategyFuncFeed = ManholeStrategy('inputManholeStrFeed1','inputManholeStrFeed2','inputManholeStrFeed3','btn_inputManhole_cost2_Feed','btn_inputManhole_cost3_Feed','btn_manholeNewCostsFeed');
		var manholeParamAsBinaryFeed = manholeStrategyFuncFeed[0]; // array with binar values
		var d_feeder = manholeStrategyFuncFeed[1]; // manhole strategy


		// ACQUIRING VALUES FROM THE FORM
        // General Information
        var COname = $('#inputName').val();
        var scenarioName = $('#inputDescription').val();
		// For clustering
        var numberOfClusters = $('#inputNumClusters').val(); // calculate the number of KV (clusters)
		var shapeFilePath = $('#inputShp').val();
		// For distribution network
		var capList = $('#inputSubductsDist').val();
		var capListCost = $('#inputCostCableGranDist').val();
		var KVcost = $('#inputcostKVDist').val();
		var lmin = $('#inputminDistDist').val();
		var lmax = $('#inputmaxDistDist').val();
		var mhn_cost = $('#inputManHoleCostDist').val();
		var mhn_c_l = "["+manholeParamAsBinaryDist+"]"; //parameters for manhole strategy 
		var d = d;
		//alert(d);
		//alert(mhn_c_l);
		
		var PercentageOfCoverageDHN = $('#inputPercentageOfCoverageDist').val();
		// For feeder network
		var capListFeeder = $('#inputSubductsFeeder').val();
		var capListCostFeeder = $('#inputCostCableGranFeeder').val();
		var CentralOfficecost = $('#inputcostCO').val();
		var lminFeeder = $('#inputminDistFeeder').val();
		var lmaxFeeder = $('#inputmaxDistFeeder').val();
		var mhn_costFeeder = $('#inputManHoleCostFeeder').val();
		var mhn_c_l_feeder = "["+manholeParamAsBinaryFeed+"]"; //parameters for manhole strategy 
		var d_feeder = d_feeder;
		
		// NESTED AJAX REQUESTS
		//////////////////////////
		//Ajax request for Cluster
		//////////////////////////
        $.ajax({
			type: "POST",
			url: 'Code/clusterExec.php',
			data: {numberOfClusters:numberOfClusters,shapeFilePath:shapeFilePath, PercentageOfCoverageDHN:PercentageOfCoverageDHN,COname:COname,scenarioName:scenarioName},
			success: function(cls000){
				//console.log(cls000); # cluster coordinates 
				//alert(cls000)
				$(".progress-bar").css("width", "30%");
				$(".progress-bar").text('Clustering Done!');
				// Check if the text forms for Distribution Network are filled
				if (capList !='' && capListCost!='' && KVcost!='' && lmin!='' && lmax!='' && mhn_cost!=''){	
					///////////////////////////////////////
					//Ajax request for Distribution Network
					///////////////////////////////////////
					$.ajax({
						type: "POST",
						url: 'Code/distributionNetExec.php',
						data: {numberOfClusters:numberOfClusters,shapeFilePath:shapeFilePath,capList:capList, capListCost:capListCost, KVcost:KVcost, lmin:lmin,lmax:lmax, mhn_cost:mhn_cost, PercentageOfCoverageDHN:PercentageOfCoverageDHN, mhn_c_l:mhn_c_l, d:d,COname:COname,scenarioName:scenarioName},
						success: function(cls000){
							console.log(cls000);
                            //alert(cls000)
							$(".progress-bar").css("width", "80%");
							$(".progress-bar").text('Distribution Network Done!');
							
							// Check if the text forms for Feeder Network are filled
							if(capListFeeder !='' && capListCostFeeder!='' && CentralOfficecost!='' && lminFeeder!='' && lmaxFeeder!='' && mhn_costFeeder!=''){
								///////////////////////////////////////
								//Ajax request for Feeder Network
								///////////////////////////////////////
								$.ajax({
									type: "POST",
									url: 'Code/feederNetExec.php',
									data: {numberOfClusters:numberOfClusters,shapeFilePath:shapeFilePath, capListFeeder:capListFeeder, capListCostFeeder:capListCostFeeder, CentralOfficecost:CentralOfficecost, lminFeeder:lminFeeder, lmaxFeeder:lmaxFeeder, mhn_costFeeder:mhn_costFeeder, mhn_c_l_feeder:mhn_c_l_feeder,d_feeder:d_feeder, PercentageOfCoverageDHN:PercentageOfCoverageDHN,COname:COname,scenarioName:scenarioName},
									success: function(cls000){
										//alert(cls000);
										console.log(cls000);
										$(".progress-bar").css("width", "100%");
										$(".progress-bar").text('Feeder Network Done!');
									},
									error: function(){
										alert("failure");
									}
								});	
							}else{
								alert("Missing Data for Feeder Network Algorithm");
							} //end else
						},
						error: function(){
							alert("failure");
						}
					});	
				}else{
					alert("Missing Data for Distribution Network Algorithm");
				}
			}, // end of success function AJAX_I
			error: function(){
				alert("failure");
			}
       });
      
	}); 
	});
	</script>
  
    
    
	<!-- ENTER DEFAULT VALUES TO TEXT FIELDS ON DEFAULT BUTTON CLICK -->
	<script>	
	$(document).ready(function(){
		$("#btnDefaultVal").click(function(){
            // For general part (Scenario name etc.)
            $('#inputName').val('CentralOffice');
            $('#inputDescription').val('3Clusters_SouthLarissa');
			// For cluster part
            $('#inputTotalPopulation').val(2000);
            $('#inputKVcapacity').val(240);
            $('#inputNumClusters').val(9);
			$('#inputShp').val('python/inputShp/larissa_subset/larissa_dimitris_subset.shp');
			// For Distribution network (DHN) part
			$('#inputSubductsDist').val('[1,2,4,8,24,48,96,144],[1],[7,24],[1]');
			$('#inputCostCableGranDist').val('[1.0,1.08,1.15,1.2,1.24,1.3,1.4,1.48],[0.0],[2,3],[1]');
			$('#inputcostKVDist').val(3000);
			$('#inputminDistDist').val(0);
			$('#inputmaxDistDist').val(2000);
			$('#inputManHoleCostDist').val('[20,100,500,100,500,20,100,500]');
			$('#inputManholeStrDist3').prop('checked', true); // checkboxes set true
			$("#btn_inputManhole_cost3_Dist").removeClass('hidden'); // make dropdownmenu visible
			$('#btn_inputManhole_cost3_Dist').text('Low Cost'); // set dropdown menu
			// For central office part
			$('#inputSubductsFeeder').val('[96,192],[1],[7,14],[1]');
			$('#inputCostCableGranFeeder').val('[1.15,1.40],[0.0],[2,3],[1]');
			$('#inputcostCO').val(10000);
			$('#inputminDistFeeder').val(0);
			$('#inputmaxDistFeeder').val(500);
			$('#inputManHoleCostFeeder').val('[20,100,500,100,500,20,100,500]');
			$('#inputManholeStrFeed2').prop('checked', true); // checkboxes set true
			$("#btn_inputManhole_cost2_Feed").removeClass('hidden'); // make dropdownmenu visible
			$('#btn_inputManhole_cost2_Feed').text('Low Cost'); // set dropdown menu
			// Reseting progresbar
			$(".progress-bar").css("width", "0%");
			$(".progress-bar").text('');
		});
	});
	</script>
	
	
	<!-- RESET VALUES FROM DROPDOWN MENU ON RESET BUTTON CLICK -->
	<script>	
	$(document).ready(function(){
        
		$("#resetBtnId").click(function(){
			$('#btn_inputManhole_cost2_Dist').text('LC/HC'); // set dropdown menu for distribution
			$("#btn_inputManhole_cost2_Dist").addClass('hidden'); // make dropdownmenu visible	
			$('#btn_inputManhole_cost3_Feed').text('LC/HC'); // set dropdown menu for feeder
			$("#btn_inputManhole_cost3_Feed").addClass('hidden'); // make dropdownmenu visible
		});
	});
	</script>
	
	
	<script>	
		<!-- GET THE VALUE OF DROPDOWN MENU AND PLACE IT TO TEXTFIELD -->
		$(document).ready(function(){
			
			$('.demolist').on('click', function(){
				var partPath =  $(this).find("a").text(); // GET THE VALUE OF DROPDOWN MENU AND PLACE IT TO TEXTFIELD
				var wholePath = 'python/inputShp/larissa_subset/'+partPath;
				$('#inputShp').val(wholePath);
				$("#dropdown-menu-id").dropdown("toggle"); // CLOSE THE DROPDOWN MENU AFTER SELECTION
				return false;
			});
			
		});
		
		<!-- CHANGE THE VALUE OF DROPDOWN MENUS (FOR MANHOLES) BASED ON WHAT YOU SELECT	-->
		$(function(){
			// For distribution network
			var manholeParameters = 'none';
			$("#ul_manholeNewCosts li a").click(function(){
				$("#btn_manholeNewCosts:first-child").text($(this).text());
				$("#btn_manholeNewCosts:first-child").val($(this).text());
				//alert($( "#manholeStr" ).text());
				manholeParameters = $( "#btn_manholeNewCosts" ).text();
			});
			$("#ul_inputManhole_cost3_Dist li a").click(function(){
				$("#btn_inputManhole_cost3_Dist:first-child").text($(this).text());
				$("#btn_inputManhole_cost3_Dist:first-child").val($(this).text());
				//alert($( "#manholeStr" ).text());
				manholeParameters = $( "#btn_inputManhole_cost3_Dist" ).text();
			});
			$("#ul_inputManhole_cost2_Dist li a").click(function(){
				$("#btn_inputManhole_cost2_Dist:first-child").text($(this).text());
				$("#btn_inputManhole_cost2_Dist:first-child").val($(this).text());
				//alert($( "#manholeStr" ).text());
				manholeParameters = $( "#btn_inputManhole_cost2_Dist" ).text();
			});
			
			// For feeder network
			$("#ul_manholeNewCostsFeed li a").click(function(){
				$("#btn_manholeNewCostsFeed:first-child").text($(this).text());
				$("#btn_manholeNewCostsFeed:first-child").val($(this).text());
				manholeParameters = $( "#btn_manholeNewCostsFeed" ).text();
			});
			$("#ul_inputManhole_cost3_Feed li a").click(function(){
				$("#btn_inputManhole_cost3_Feed:first-child").text($(this).text());
				$("#btn_inputManhole_cost3_Feed:first-child").val($(this).text());
				manholeParameters = $( "#btn_inputManhole_cost3_Dist" ).text();
			});
			$("#ul_inputManhole_cost2_Feed li a").click(function(){
				$("#btn_inputManhole_cost2_Feed:first-child").text($(this).text());
				$("#btn_inputManhole_cost2_Feed:first-child").val($(this).text());
				manholeParameters = $( "#btn_inputManhole_cost2_Feed" ).text();
			});
		});
		
		<!-- MANAGE THE PARAMETERS FOR MANHOLE STRATEGY AND COST TYPES	-->
		$(document).ready(function(){
			// If a 2way or 3way strategy is selected then the dropdown menu LC/HC 
			// corresponding appears.
			// For distribution network
			$('.cbManholeDist').change(function(){
				if ($('#inputManholeStrDist3').is(':checked')) {
					$("#btn_inputManhole_cost3_Dist").removeClass('hidden');
				}
				else {
					$("#btn_inputManhole_cost3_Dist").text('LC/HC'); // reset value on button
					$("#btn_inputManhole_cost3_Dist").addClass('hidden');	
				}
				if ($('#inputManholeStrDist2').is(':checked')) {
					$("#btn_inputManhole_cost2_Dist").removeClass('hidden');
				}
				else {
					$("#btn_inputManhole_cost2_Dist").text('LC/HC'); // reset value on button
					$("#btn_inputManhole_cost2_Dist").addClass('hidden');
				}
			}) 	
			// For feeder network
			$('.cbManholeFeed').change(function(){
				if ($('#inputManholeStrFeed3').is(':checked')) {
					$("#btn_inputManhole_cost3_Feed").removeClass('hidden');
				}
				else {
					$("#btn_inputManhole_cost3_Feed").text('LC/HC'); // reset value on button
					$("#btn_inputManhole_cost3_Feed").addClass('hidden');	
				}
				if ($('#inputManholeStrFeed2').is(':checked')) {
					$("#btn_inputManhole_cost2_Feed").removeClass('hidden');
				}
				else {
					$("#btn_inputManhole_cost2_Feed").text('LC/HC'); // reset value on button
					$("#btn_inputManhole_cost2_Feed").addClass('hidden');
				}
			}) 			
		});
	</script>
    
    
    
    <!-- DISPLAY THE CALCULATED NUMBER OF CABINETS (ON THE INPUT FORM)-->
    <script>	
	$(document).ready(function(){
        // get input values from input fields
        $( "#inputTotalPopulation, #inputKVcapacity " ).keyup(function() {
            var population = $('#inputTotalPopulation').val();
            var KVcapacity = $('#inputKVcapacity').val();
            if (KVcapacity != '' && population!= ''){   
                var calculatedCabins = Math.ceil(population/KVcapacity);
                $('#inputNumClusters').val(calculatedCabins); 
            }
        });
	});
	</script>
    
    
    
</body>
</html>


