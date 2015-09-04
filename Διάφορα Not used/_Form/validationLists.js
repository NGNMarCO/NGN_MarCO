// Validation for:
// NUM IF SYBDUCTS IN DUCTS FOR DISTRIBUTION NETWORK
// NUM IF SYBDUCTS IN DUCTS FOR FEEDER NETWORK
// Cable granularity for Feeder Network
// Cable granularity for Distribution Network

// Takes as input the: sheet variable, a string with the values inserted in the form, the column number of the cell in the form

function validationList(sheet,integerStringArray,rowNum,validationArr){
	
	if (integerStringArray===null ){
	//alert(typeof integerStringArray);
		sheet.setValue(rowNum, 2, "Enter values in this form [1,2,3..]"); 
		sheet.getCell(rowNum,2).foreColor("white");
		sheet.getCell(rowNum,2).backColor("red");
		validationArr.push(0);
	}
	else if (integerStringArray!==null) {
		//alert(typeof integerStringArray);
		integerStringArray = String(integerStringArray); // convert value to string
		sheet.getCell(rowNum,2).foreColor("black");
		sheet.getCell(rowNum,2).backColor("#FFCC99");
	
		var Indexcomma = integerStringArray.indexOf(",");
		// HANDLE IF THE VALUE IS SINGLE
		if (Indexcomma==-1) { //doesn't exist
			var checkVar = isNaN(integerStringArray);
			if (checkVar === false){
				validationArr.push(1);
				sheet.getCell(rowNum,2).foreColor("black");
				sheet.getCell(rowNum,2).backColor("green");	
			}
			else if (checkVar===true){
				sheet.setValue(rowNum, 2, "Enter values in this form [1,2,3..]"); 
				sheet.getCell(rowNum,2).foreColor("white");
				sheet.getCell(rowNum,2).backColor("red");
				validationArr.push(0);
			}
		}
		// HANDLE IF THE VALUE IS MULTIPLE (COMMAS)
		else if (Indexcomma!==-1) { // comma exists
			var SplittArr = integerStringArray.split(",");
			for (var i = 0; i < SplittArr.length; i++) { // check if all characters are numbers
				var checkVar = isNaN(SplittArr[i]);
				//alert(checkVar);
				if (checkVar ===false){
					validationArr.push(1);
					//alert(x);
					sheet.getCell(rowNum,2).foreColor("black");
					sheet.getCell(rowNum,2).backColor("green");	
				}
				else if (checkVar ===true){
					sheet.setValue(rowNum, 2, "Enter values in this form [1,2,3..]"); 
					sheet.getCell(rowNum,2).foreColor("white");
					sheet.getCell(rowNum,2).backColor("red");
					validationArr.push(0);
					//alert(x);
					break;
				}
			}
		}	
	}
	return validationArr; // return an array with all the values
}
