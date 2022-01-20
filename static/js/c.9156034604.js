setInterval(function(){ // load the data from your endpoint into the div
     $("#orders-managed").load("/get_managed")
},1000)

setInterval(function(){ // load the data from your endpoint into the div
     $("#weekly-orders").load("/get_weekly")
},1000)

setInterval(function(){ // load the data from your endpoint into the div
     $("#orders-delivered").load("/get_delivered")
},1000)

setInterval(function(){ // load the data from your endpoint into the div
     $("#orders-sent").load("/get_sent")
},1000)

setInterval(function(){ // load the data from your endpoint into the div
     $("#current-delivery").load("/get_msg")
},1000)

function buttonDelivery() {
  if (document.getElementById("delivery-msg").value.length == 0) {
    var del_val = document.getElementById("delivery-msg").style.backgroundColor;
    document.getElementById("delivery-msg").style.backgroundColor = '#ff5252';
    setTimeout(function() {
         document.getElementById("delivery-msg").style.backgroundColor = del_val;
    }, 1500);
  }
  else {
    document.getElementById("delivery-button").disabled = true;
  	document.getElementById("delivery-button").innerHTML = "<div id='spinner-load' class='spinner-border text-warning'></div>"
    var dm = document.getElementById("delivery-msg").value;
    $.post("/delivery_msg", {
        delivery_message: dm
    }).done(
    function(response){
        document.getElementById("modalTitle").innerHTML = "SUCCESS";
        document.getElementById("modalBody").innerHTML = response;
        $("#myModal").modal('show');
        document.getElementById("delivery-button").disabled = false;
        document.getElementById("delivery-button").innerHTML = "SET DELIVERY MESSAGE"
        document.getElementById("delivery-msg").value = ""
     })
     .fail(
     function(response){
        document.getElementById("modalTitle").innerHTML = "ERROR";
        document.getElementById("modalBody").innerHTML = response.responseText;
        $("#myModal").modal('show');
        document.getElementById("delivery-button").disabled = false;
      	document.getElementById("delivery-button").innerHTML = "SET DELIVERY MESSAGE"
      });
  }
}

function resignPopup() {
  $("#resignBox").modal('show');
}

function resignConfirm() {
  document.getElementById("buttonStay").disabled = true;
  document.getElementById("buttonResign").disabled = true;
  document.getElementById("buttonResign").innerHTML = "<div id='spinner-load' class='spinner-border text-warning'></div>"
  $.post("/resign_user", {
  }).done(
  function(response){
    location.replace(response);
   })
   .fail(
   function(response){
      document.getElementById("modalTitle").innerHTML = "ERROR";
      document.getElementById("modalBody").innerHTML = response.responseText;
      $("#myModal").modal('show');
      document.getElementById("buttonStay").disabled = false;
      document.getElementById("buttonResign").disabled = false;
      document.getElementById("buttonResign").innerHTML = "RESIGN NOW"
    });
}
