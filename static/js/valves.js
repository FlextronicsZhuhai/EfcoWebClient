$(document).ready(function() {
    $('#valves').DataTable();
    $('#deleteValve').on('click',function(e){
      e.preventDefault();
      var input=window.prompt('Enter the Valve ID');
      var confirm=window.confirm('Are you sure to delete '+input+' valve?');

      if(confirm == true){
        var request = $.ajax({
      		url: "http://localhost:5000/deleteRPSLValve",
      		method: "POST",
      		data: {
      			"valve_id":input,
      		}
      	});

      	request.done(function( msg ) {
          $('#alert-box').css('display',"block");
      		$( "#message" ).html( msg.message);
          setTimeout(location.reload(),1000);
      	});

      	request.fail(function( jqXHR, textStatus ) {
      		alert( "Request failed: " + textStatus );
      	});
      }
    });
} );
