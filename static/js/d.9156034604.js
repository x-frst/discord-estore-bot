function buttonApplication() {
  if (document.getElementById("application-form").value.length == 0) {
    var app_val = document.getElementById("application-form").style.backgroundColor;
    document.getElementById("application-form").style.backgroundColor = '#ff5252';
    setTimeout(function() {
         document.getElementById("application-form").style.backgroundColor = app_val;
    }, 1500);
  }
  else {
    document.getElementById("application-button").disabled = true;
  	document.getElementById("application-button").innerHTML = "<div id='spinner-load' class='spinner-border text-warning'></div>"
    var app = document.getElementById("application-form").value;
    $.post("/user_application", {
        application_reason: app
    }).done(
    function(response){
        document.getElementById("modalTitle").innerHTML = "SUCCESS";
        document.getElementById("modalBody").innerHTML = response;
        $("#myModal").modal('show');
        document.getElementById("application-button").disabled = false;
        document.getElementById("application-button").innerHTML = "SEND APPLICATION"
        document.getElementById("application-form").value = "";
     })
     .fail(
     function(response){
       document.getElementById("modalTitle").innerHTML = "ERROR";
       document.getElementById("modalBody").innerHTML = response.responseText;
       $("#myModal").modal('show');
       document.getElementById("application-button").disabled = false;
       document.getElementById("application-button").innerHTML = "SEND APPLICATION"
      });
  }
}
