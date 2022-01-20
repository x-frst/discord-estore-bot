function buttonAppeal() {
  if (document.getElementById("ban-reason").value.length == 0) {
    var app_val = document.getElementById("ban-reason").style.backgroundColor;
    document.getElementById("ban-reason").style.backgroundColor = '#ff5252';
    setTimeout(function() {
         document.getElementById("ban-reason").style.backgroundColor = app_val;
    }, 1500);
  }
  if (document.getElementById("ban-chance").value.length == 0) {
    var app_val = document.getElementById("ban-chance").style.backgroundColor;
    document.getElementById("ban-chance").style.backgroundColor = '#ff5252';
    setTimeout(function() {
         document.getElementById("ban-chance").style.backgroundColor = app_val;
    }, 1500);
  }
  if (document.getElementById("ban-reason").value.length != 0 && document.getElementById("ban-chance").value.length != 0) {
    document.getElementById("appeal-button").disabled = true;
  	document.getElementById("appeal-button").innerHTML = "<div id='spinner-load' class='spinner-border text-warning'></div>"
    if (document.getElementById('guildBan').checked) {
      var ban_type = "Guild Ban"
    }
    else {
      var ban_type = "Bot Account Flagged"
    }
    var chance = document.getElementById("ban-chance").value;
    var reason = document.getElementById("ban-reason").value;
    $.post("/user_appeal", {
        appeal_type: ban_type,
        appeal_chance: chance,
        appeal_reason: reason
    }).done(
    function(response){
        document.getElementById("modalTitle").innerHTML = "SUCCESS";
        document.getElementById("modalBody").innerHTML = response;
        $("#myModal").modal('show');
        document.getElementById("appeal-button").disabled = false;
        document.getElementById("appeal-button").innerHTML = "SEND APPEAL"
        document.getElementById("ban-chance").value = "";
        document.getElementById("ban-reason").value = "";
     })
     .fail(
     function(response){
       document.getElementById("modalTitle").innerHTML = "ERROR";
       document.getElementById("modalBody").innerHTML = response.responseText;
       $("#myModal").modal('show');
       document.getElementById("appeal-button").disabled = false;
       document.getElementById("appeal-button").innerHTML = "SEND APPEAL"
      });
  }
}
