// Validation for:
// Max and Min distances for Manholes For Feeder and Distribution Strategy


// Takes as input the: sheet variable, a string with the values inserted in the form, the column and row number of the cell in the form

function validationManDist(sheet,Distance,rowNum, columNum,validationArr){
	
	if (Distance===null ){
	//alert(typeof Distance);
		sheet.setValue(rowNum, columNum, "Enter distance"); 
		sheet.getCell(rowNum,columNum).foreColor("white");
		sheet.getCell(rowNum,columNum).backColor("red");
		validationArr.push(0);	
	}
	else if(Distance!==null){
		var checkVar = isNaN(Distance);
		if (checkVar ===false){
			validationArr.push(1);
			//alert(x);
			sheet.getCell(rowNum,columNum).foreColor("black");
			sheet.getCell(rowNum,columNum).backColor("green");	
		}
		else if (checkVar ===true){
			sheet.setValue(rowNum, columNum, "Enter distance"); 
			sheet.getCell(rowNum,columNum).foreColor("white");
			sheet.getCell(rowNum,columNum).backColor("red");
			validationArr.push(0);
			//alert(x);
		}
	}
	return validationArr; // return an array with all the values
}
