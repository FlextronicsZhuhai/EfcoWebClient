$(document).ready(function(){
	$('#startRPVI').on('click',function(event){
		event.preventDefault();
		alert("hello");
		var confirm=$.ajax({
			url:"/startRPVI",
			method:"GET",
			headers:{'Access-Control-Allow-Origin':'*'},
			crossDomain: true
		});
		confirm.done(function(msg){
		alert(msg);
		});
		confirm.fail(function(jqXHR,textStatus){
			alert( "Request failed: " + textStatus );
		});
	});
	$('#startSLVI').on('click',function(event){
		event.preventDefault();
		alert("hello");
		var confirm=$.ajax({
			url:"/startSLVI",
			method:"GET",
			headers:{'Access-Control-Allow-Origin':'*'},
			crossDomain: true
		});
		confirm.done(function(msg){
		alert(msg);
		});
		confirm.fail(function(jqXHR,textStatus){
			alert( "Request failed: " + textStatus );
		});
	});
	$('#rpTest').on('click',function(event){
		event.preventDefault();
		var targetPressure=$('#targetPressure').val();
		var minimumTolerance=$('#minimumTolerance').val();
		var maximumTolerance=$('#maximumTolerance').val();

	var request = $.ajax({
		url: "http://127.0.0.1:8023/EfcoDataAcquisition/releasePressure",
		method: "GET",
		data: {
			"targetPressure":targetPressure,
			"maximumTolerance": maximumTolerance,
			"minimumTolerance": minimumTolerance
		},
		crossDomain: true
	});

	request.done(function( msg ) {
		console.log(msg);
		$( "#actualReleasePressure" ).val( msg.maximumPressure);

	});

	request.fail(function( jqXHR, textStatus ) {
		alert( "Request failed: " + textStatus );
	});
	});

	$('#slTest').on('click',function(event){
		event.preventDefault();
		var time=$('#time').val();
		var testPressure=$('#actualReleasePressure').val()*(~~($('#percentageRelease').val()))/100;


	var request = $.ajax({
		url: "http://127.0.0.1:8023/EfcoDataAcquisition/seatLeakage",
		method: "GET",
		data: {
			"time":time,
			"testPressure":testPressure,
		},
		crossDomain: true
	});

	request.done(function( msg ) {
		console.log(msg);
		$( "#finalPressure" ).val( msg.finalPressure);

	});

	request.fail(function( jqXHR, textStatus ) {
		alert( "Request failed: " + textStatus );
	});
	});

});
