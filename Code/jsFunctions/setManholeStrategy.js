// The javascript function setManholeStrategy takes as input the ids of the checkboxes of the manhole strategy
// and returns an array of length 8, which has binary values (0 or 1). This array is later used in 
// the distribution network and feeder network algorithms. 
// Also it returns the parameter: "d" which defines the mahole strategy to be used based on the user's selection.


function ManholeStrategy(ManholeStrDist1, ManholeStrDist2, ManholeStrDist3, btn_inputManhole_cost2_Dist, btn_inputManhole_cost3_Dist, btn_manholeNewCosts) {

    // Manage the Parameters for the Manholes for Distribution
		var manholeParamAsBool = [];
		var manholeParamAsBinary = [];
		manholeParam = $('#'+ManholeStrDist1).is(':checked');manholeParamAsBool.push(manholeParam);
		manholeParam = $('#'+ManholeStrDist2).is(':checked');manholeParamAsBool.push(manholeParam);
		manholeParam = $('#'+ManholeStrDist3).is(':checked');manholeParamAsBool.push(manholeParam);
		manholeParam = $('#'+btn_inputManhole_cost2_Dist).text();manholeParamAsBool.push(manholeParam);
		manholeParam = $('#'+btn_inputManhole_cost3_Dist).text();manholeParamAsBool.push(manholeParam);
		manholeParam = $('#'+btn_manholeNewCosts).text();manholeParamAsBool.push(manholeParam);
		// For 1 way
		if (manholeParamAsBool[0] === true){
				var mhn_c_l_1 = 1;
				manholeParamAsBinary.push(mhn_c_l_1);
		}
		 else{
				var mhn_c_l_1 = 0;
				manholeParamAsBinary.push(mhn_c_l_1);
		}
		// For 2 way
		if (manholeParamAsBool[1] === true && manholeParamAsBool[3] == 'Low Cost'){
				var mhn_c_l_2 = 1;
				var mhn_c_l_3 = 0;
				manholeParamAsBinary.push(mhn_c_l_2);manholeParamAsBinary.push(mhn_c_l_3);
		}else if (manholeParamAsBool[1] === true && manholeParamAsBool[3] == 'High Cost') {
				var mhn_c_l_2 = 0;
				var mhn_c_l_3 = 1;
				manholeParamAsBinary.push(mhn_c_l_2);manholeParamAsBinary.push(mhn_c_l_3);
		}
		else if (manholeParamAsBool[1] === true && manholeParamAsBool[3] == 'LC/HC'){
				alert('Select a value from the menu');
		}
		else{
				var mhn_c_l_2 = 0;
				var mhn_c_l_3 = 0;
				manholeParamAsBinary.push(mhn_c_l_2);manholeParamAsBinary.push(mhn_c_l_3);
		}
		// For 3 way
		if (manholeParamAsBool[2] === true && manholeParamAsBool[4] == 'Low Cost'){
				var mhn_c_l_4 = 1;
				var mhn_c_l_5 = 0;
				manholeParamAsBinary.push(mhn_c_l_4);manholeParamAsBinary.push(mhn_c_l_5);
		}else if (manholeParamAsBool[2] === true && manholeParamAsBool[4] == 'High Cost'){
				var mhn_c_l_4 = 0;
				var mhn_c_l_5 = 1;
				manholeParamAsBinary.push(mhn_c_l_4);manholeParamAsBinary.push(mhn_c_l_5);			
		}
		else if (manholeParamAsBool[2] === true && manholeParamAsBool[4] == 'LC/HC'){
				alert('Select a value from the menu');
		}
		else{
				var mhn_c_l_4 = 0;
				var mhn_c_l_5 = 0;
				manholeParamAsBinary.push(mhn_c_l_4);manholeParamAsBinary.push(mhn_c_l_5);
		}
		// For new manhole costs
		if (manholeParamAsBool[5] == 'Cheap'){
				var mhn_c_l_6 = 1;
				var mhn_c_l_7 = 0;
				var mhn_c_l_8 = 0;
				manholeParamAsBinary.push(mhn_c_l_6);manholeParamAsBinary.push(mhn_c_l_7);manholeParamAsBinary.push(mhn_c_l_8);
		}else if (manholeParamAsBool[5] == 'Average'){
				var mhn_c_l_6 = 0;
				var mhn_c_l_7 = 1;
				var mhn_c_l_8 = 0;
				manholeParamAsBinary.push(mhn_c_l_6);manholeParamAsBinary.push(mhn_c_l_7);manholeParamAsBinary.push(mhn_c_l_8);
		}
		else {
				var mhn_c_l_6 = 0;
				var mhn_c_l_7 = 0;
				var mhn_c_l_8 = 1;
				manholeParamAsBinary.push(mhn_c_l_6);manholeParamAsBinary.push(mhn_c_l_7);manholeParamAsBinary.push(mhn_c_l_8);
		}
		
		// Create the parameter "d" which indicates the type of strategy. Possible values: 3, 2, 1, 32, 31, 21, 321
		if (manholeParamAsBool[0] === true && manholeParamAsBool[1] === false && manholeParamAsBool[2] === false) {
			var d = 1;
		} else if (manholeParamAsBool[0] === false && manholeParamAsBool[1] === true && manholeParamAsBool[2] === false){
			var d = 2;
		} else if (manholeParamAsBool[0] === false && manholeParamAsBool[1] === false && manholeParamAsBool[2] === true){
			var d = 3;	
		}else if (manholeParamAsBool[0] === false && manholeParamAsBool[1] === true && manholeParamAsBool[2] === true){
			var d = 32;
		}else if (manholeParamAsBool[0] === true && manholeParamAsBool[1] === false && manholeParamAsBool[2] === true){
			var d = 31;
		}
		else if (manholeParamAsBool[0] === true && manholeParamAsBool[1] === true && manholeParamAsBool[2] === false){
			var d = 21;
		}else if (manholeParamAsBool[0] === true && manholeParamAsBool[1] === true && manholeParamAsBool[2] === true){
			var d = 321;
		}

    return [manholeParamAsBinary, d];  
}








