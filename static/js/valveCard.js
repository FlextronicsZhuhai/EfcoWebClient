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
			$(".selectLengthUnit").attr('disabled',false);
			editing=1;
		}
		else {
			editing=0;
			$('#editValve').html('<i class="fa fa-pencil"></i> Edit Valve');
			$('#updateValveData').css('display',"none");
			$('#updateRPSLValveTechData').css('display',"none");
			$('input:text').attr('disabled',true);
			$('#minimumTolerance, #maximumTolerance, #targetPressure, #time, #percentageRelease').attr('disabled',false);
			$(".selectLengthUnit").attr('disabled',true);
		}
	});
	$('#generateReport').on('click',function(e){
		e.preventDefault();
		$('#rtargetPressure').val($('#targetPressure').val());
		$('#ractualPressure').val($('#actualReleasePressure').val());
		$('#rfinalPressure').val($('#finalPressure').val());
		$('#rvalve_id').val($('#valveNumber').val());
		
			var comment=window.prompt("Enter your comment");
		var request = $.ajax({
			url: "http://localhost:5000/generateReport",
			method:"POST",
			type:"POST",
			data:{
				"valve_id":$('#valveNumber').val(),
				"valve_type":$('#valve_type').val(),
				"dnInlet":$('#dnInlet').val(),
				"dnInletUnit":$('#dnInletUnit').val(),
				"dnOutlet":$('#dnOutlet').val(),
				"dnOutletUnit":$('#dnOutletUnit').val(),
				"seatPressure":$('#seatPressure').val(),
				"seatPressureUnit":$('#seatPressureUnit').val(),
				"seatDiameter":$('#seatDiameter').val(),
				"axMeasurement":$('#axMeasurement').val(),
				"inspector":$('#inspector').val(),
				"applicationNumber":$('#applicationNumber').val(),
				"certificationNumber":$('#certificationNumber').val(),
				"testLocation":$('#testLocation').val(),
				"surveyor":$('#surveyor').val(),
				"testDate":$('#testDate').val(),
				"testMedium":$('#testMedium').val(),
				"pressureTransducer":$('#pressureTransducer').val(),
				"minimumTolerance":$('#minimumTolerance').val(),
				"maximumTolerance":$('#maximumTolerance').val(),
				"targetReleasePressure":$('#targetPressure').val(),
				"actualReleasePressure":$('#actualReleasePressure').val(),
				"slTime":$('#time').val(),
				"percentageRelease":$('#percentageRelease').val(),
				"finalPressure":$('#finalPressure').val(),
				"btTolerance":$('#btTolerance').val(),
				"btTime":$('#btTime').val(),
				"nominalPressure":$('#nominalPressure').val(),
				"btActualPressure":$('#btActualPressure').val(),
				"comments":comment
			}
		});

				request.done(function( msg ) {
					$('#alert-box').css('display','block');
					$('#message').html(msg.message);
					$('#showReport').show();
					$('#generateReport').hide();
					$('#showReport').attr('href',"/showReport/"+msg.certificationNumber+"/"+msg.valve_type);
				});


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
				"seatPressure":$('#seatPressure').val(),
				"seatPressureUnit":$('#seatPressureUnit').val(),
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
		var confirm=$.ajax({
			url:"/startRPVI",
			method:"GET",
			headers:{'Access-Control-Allow-Origin':'*'},
			crossDomain: true
		});
		confirm.done(function(msg){
		console.log(msg);
		});
		confirm.fail(function(jqXHR,textStatus){
			alert( "Request failed: " + textStatus );
		});
	});
	$('#startSLVI').on('click',function(event){
		event.preventDefault();
		var confirm=$.ajax({
			url:"/startSLVI",
			method:"GET",
			headers:{'Access-Control-Allow-Origin':'*'},
			crossDomain: true
		});
		confirm.done(function(msg){
		console.log(msg);
		});
		confirm.fail(function(jqXHR,textStatus){
			alert( "Request failed: " + textStatus );
		});
	});
	$('#startBTVI').on('click',function(event){
		event.preventDefault();

		var confirm=$.ajax({
			url:"/startBTVI",
			method:"GET",
			headers:{'Access-Control-Allow-Origin':'*'},
			crossDomain: true
		});
		confirm.done(function(msg){
		console.log(msg);
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
		url: "http://127.0.0.1:8023/EfcoWebService/releasePressure",
		method: "GET",
		data: {
			"targetPressure":targetPressure,
			"maximumTolerance": maximumTolerance,
			"minimumTolerance": minimumTolerance
		}
		});

	request.done(function( msg ) {
		console.log(msg);
		$( "#actualReleasePressure" ).val( msg.maximumPressure);
		$('#seatLeakage').show();
		$('#startSLVI').show();
		$('#slTest').show();
	});

	request.fail(function( jqXHR, textStatus ) {
		alert( "Request failed: " + textStatus );
	});
	});

	$('#slTest').on('click',function(event){
		event.preventDefault();
		var time=$('#time').val();
		var percentageRelease=~~$('#percentageRelease').val();
		if(percentageRelease>0)
		var testPressure=$('#actualReleasePressure').val()*(~~($('#percentageRelease').val()))/100;
		else {
			var testPressure=$('#testPressure').val();
		}

	var request = $.ajax({
		url: "http://127.0.0.1:8023/EfcoWebService/seatLeakageTest",
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
	$('#btTest').on('click',function(event){
		event.preventDefault();
		var time=$('#testDuration').val();
		var tolerance=$('#tolerance').val();
		var nominalPressure=$('#nominalPressure').val()*(~~(tolerance))/100;


	var request = $.ajax({
		url: "http://127.0.0.1:8023/EfcoWebService/bodyTest",
		method: "GET",
		data: {
			"time":time,
			"nominalPressure":nominalPressure,
		},
		crossDomain: true
	});

	request.done(function( msg ) {
		console.log(msg.actualPressure);
		$( "#actualPressure" ).val( msg.actualPressure);
		$('#seatLeakage').show();
		$('#startSLVI').show();
		$('#slTest').show();
	});

	request.fail(function( jqXHR, textStatus ) {
		alert( "Request failed: " + textStatus );
	});
	});
	$(function () {
			$('#testDatepicker').datetimepicker();
	});
});
