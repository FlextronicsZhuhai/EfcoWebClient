$(document).ready(function(){
	var editing=0;
	$('#editValve').on('click',function(e){
		e.preventDefault();
		if (editing==0) {
			$('#editValve').html('<i class="fa fa-times"></i> Close Editing');
			$('#updateValveData').css('display',"block");
			$('#updateRPSLValveTechData').css('display',"block");
			$('input:text').attr('disabled',false);
			$('#valveNumber').attr('disabled',true);
			$('#actualReleasePressure').attr('disabled',true);
			$('#finalPressure').attr('disabled',true);
			editing=1;
		}
		else {
			editing=0;
			$('#editValve').html('<i class="fa fa-pencil"></i> Edit Valve');
			$('#updateValveData').css('display',"none");
			$('#updateRPSLValveTechData').css('display',"none");
			$('input:text').attr('disabled',true);
			$('#minimumTolerance, #maximumTolerance, #targetPressure, #time, #percentageRelease').attr('disabled',false);


		}
	});
	$('#generateReport').on('click',function(e){
		e.preventDefault();
		$('#rtargetPressure').val($('#targetPressure').val());
		$('#ractualPressure').val($('#actualReleasePressure').val());
		$('#rfinalPressure').val($('#finalPressure').val());
		$('#rvalve_id').val($('#valveNumber').val());
		$("#reportForm").submit();
	});
	$('#updateValveData').on('click',function(e){
		e.preventDefault();
		var request = $.ajax({
			url: "http://localhost:5000/updateRPSLValve",
			method: "POST",
			data: {
				"valve_id":$('#valveNumber').val(),
				"valve_type":$("#valveType").val(),
				"rev_no":$("#rev_no").val(),
				"part_no":$("#part_no").val(),
				"plant":$("#plant").val(),
				"install_locations":$("#install_locations").val(),
				"customer":$("#customer").val(),
				"manufacturer":$("#manufacturer").val(),
				"manufacturer_no":$("#manufacturer_no").val(),
			}
		});

		request.done(function( msg ) {
			$('#alert-box').css('display','block');
			$('#message').html(msg.message);
		});

		request.fail(function( jqXHR, textStatus ) {
			alert( "Request failed: " + textStatus );
		});
	});
	$('#updateRPSLValveTechData').on('click',function(e){
		e.preventDefault();
		var request = $.ajax({
			url: "http://localhost:5000/updateRPSLValveTechData",
			method: "POST",
			data: {
				"valve_id":$('#valveNumber').val(),
				"dnInlet":$('#dnInlet').val(),
				"dnInletUnit":$('#dnInletUnit').val(),
				"dnOutlet":$('#dnOutlet').val(),
				"dnOutletUnit":$('#dnOutletUnit').val(),
				"setPressure":$('#setPressure').val(),
				"setPressureUnit":$('#setPressureUnit').val(),
				"seatDiameter":$('#seatDiameter').val(),
				"axMeasurement":$('#axMeasurement').val()
			}
		});

		request.done(function( msg ) {
			$('#alert-box').css('display','block');
			$('#message').html(msg.message);
		});

		request.fail(function( jqXHR, textStatus ) {
			alert( "Request failed: " + textStatus );
		});
	});
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
