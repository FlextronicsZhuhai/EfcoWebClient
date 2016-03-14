$(document).ready(function(){
	$('#newTest').on('click',function(event){
		event.preventDefault();
		var targetPressure=$('#targetPressure').val();
		var minimumTolerance=$('#minimumTolerance').val();
		var maximumTolerance=$('#maximumTolerance').val();
		var request = $.ajax({
			url: "http://127.0.0.1:8001/EfcoDAQService/EfcoBackendService",
			method: "GET",
			data: { 
				"targetPressure":targetPressure,
				"maximumTolerance": maximumTolerance,
				"minimumTolerance": minimumTolerance
				 }
		});

		request.done(function( msg ) {
			
			$( "#actualReleasePressure" ).val( msg.maximumPressure);
			
		});

		request.fail(function( jqXHR, textStatus ) {
			alert( "Request failed: " + textStatus );
		});
	});
});