function validate(mode){
	if(mode==1){
		/* userId validation */
		alert("userId");
	}	
	else if(mode==2){
		/* password validation */
	}
	else if(mode==3){
		/* email validation */
	}
	else if(mode==4){
		/* file validation */
		var fInput=document.getElementById();
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		alert(fInput.value);
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
			return false;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			return true;
		} 
        
	}
}
