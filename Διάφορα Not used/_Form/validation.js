function validation(sheet,CentralOffice,DestributionCenter,NumSubDucFeeder,NumSubDucDistrib,CableGranFeeder,CableGranDistrib,Percentages,ManholeFeedermaxDist,ManholeFeederminDist,ManholeDistribmaxDist,ManholeDistribminDist,ScenarioName,ScenarioDescription){
	// IF ONE OF THE FIELDS IS EMPTY MAKE IT RED
	var validationArr = []; // array to return
	//****************************************************************
	// CENTRAL OFFICE
	//****************************************************************
	// if the field is empty or the variable is not integer or the variable is not integer get message
	if (CentralOffice===null || typeof CentralOffice !== 'number' || ( typeof CentralOffice === 'number' && CentralOffice % 1 !== 0 ) || CentralOffice>100 ){
	//alert(typeof CentralOffice);
		sheet.setValue(5, 2, "Empty field or value not integer or value too big"); 
		sheet.getCell(5,2).foreColor("white");
		sheet.getCell(5,2).backColor("red");
		validationArr.push(0);	
	}
	else {
		sheet.getCell(5,2).foreColor("black");
		sheet.getCell(5,2).backColor("green");	
		validationArr.push(1);	
	}
	
	//****************************************************************
	// DISTRIBUTION CENTER
	//****************************************************************
	// if the field is empty or the variable is not integer or the variable is not integer get message
	if (DestributionCenter===null || typeof DestributionCenter !== 'number' || ( typeof DestributionCenter === 'number' && DestributionCenter % 1 !== 0 ) || DestributionCenter>100){
	//alert(typeof DestributionCenter);
		sheet.setValue(6, 2, "Empty field or value not integer or value too big"); 
		sheet.getCell(6,2).foreColor("white");
		sheet.getCell(6,2).backColor("red");
		validationArr.push(0);	
		//alert(validationArr);
		//validationArr.push.x;	
	}
	else {
		sheet.getCell(6,2).foreColor("black");
		sheet.getCell(6,2).backColor("green");	
		validationArr.push(1);	
		//alert(validationArr);
	}
	
	//****************************************************************
	// NUM IF SYBDUCTS IN DUCTS FOR FEEDER NETWORK
	//****************************************************************
	var ResultNumSubDucFeeder = validationList(sheet,NumSubDucFeeder,12,validationArr);
	//alert(ResultNumSubDucFeeder);

	//****************************************************************
	// NUM IF SYBDUCTS IN DUCTS FOR DISTRIBUTION NETWORK
	//****************************************************************	
	
	var ResultNumSubDucDistrib = validationList(sheet,NumSubDucDistrib,13,validationArr);

	
	//****************************************************************
	// Cable granularity for Feeder Network
	//****************************************************************	
	
	var ResultCableFeeder = validationList(sheet,CableGranFeeder,14,validationArr);
	
	//****************************************************************
	// Cable granularity for Distribution Network
	//****************************************************************	
	
	var ResultCableDistrib = validationList(sheet,CableGranDistrib,15,validationArr);
	
	//****************************************************************
	// Percentages
	//****************************************************************	
	
	var ResultPercentage = validationList(sheet,Percentages,18,validationArr);	
	
	//****************************************************************
	// MANHOLE FEEDER MAX DIST
	//****************************************************************	
	
	var ResultManFeederMax = validationManDist(sheet,ManholeFeedermaxDist,16,4,validationArr)
	
	//****************************************************************
	// MANHOLE FEEDER MIN DIST
	//****************************************************************	
	
	var ResultManFeederMin = validationManDist(sheet,ManholeFeederminDist,16,6,validationArr)
	
	//****************************************************************
	// MANHOLE FEEDER MIN DIST
	//****************************************************************	
	
	var ResultManDistribMax = validationManDist(sheet,ManholeDistribmaxDist,17,5,validationArr)
	
	//****************************************************************
	// MANHOLE FEEDER MIN DIST
	//****************************************************************	
	
	var ResultManDistribMin = validationManDist(sheet,ManholeDistribminDist,17,6,validationArr)
	
	//****************************************************************
	// SCENARIO NAME
	//****************************************************************	
	
	if (ScenarioName===null ||  ScenarioName.length>20){
		//alert(ScenarioName);
		sheet.setValue(5,9, "Missing name or name too long"); 
		sheet.getCell(5,9).foreColor("white");
		sheet.getCell(5,9).backColor("red");
		validationArr.push(0);		
	}
	else if (ScenarioName!==null && ScenarioName.length<=20 ){
		//alert(ScenarioName);
		sheet.getCell(5,9).foreColor("black");
		sheet.getCell(5,9).backColor("green");	
		validationArr.push(1);
	}
	
	//****************************************************************
	// SCENARIO DESCRIPTION
	//****************************************************************	
	//alert(ScenarioDescription);
	if (ScenarioDescription!==null && ScenarioDescription.length>100){
		//alert(ScenarioDescription);
		sheet.setValue(6,9, "Missing name or name too long"); 
		sheet.getCell(6,9).foreColor("white");
		sheet.getCell(6,9).backColor("red");	
	}
	else if (ScenarioDescription!==null && ScenarioDescription.length<=20 ){
		//alert(ScenarioDescription);
		sheet.getCell(6,9).foreColor("black");
		sheet.getCell(6,9).backColor("green");	
	}	
	else{
	
	}
	

	return validationArr; // return an array with all the values
}
