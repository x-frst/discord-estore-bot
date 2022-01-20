var buttons = 0;
var fields = 1;
let links = [];


function addImage() {
  if (fields <= 2) {
  fields++;
	var img_input = "<input type='text' placeholder='Enter image link' class='form-control' id='"+fields+"' style='margin-top:5px;transition: all 0.7s;'>";
	$("#imgField").append(img_input)
  if (buttons == 0) {
    var img_button = "<button type='button' id='removeButton' onclick='removeImage()' class='btn btn-danger' style='margin-left:10px;margin-top:10px;'>REMOVE IMAGE</button>";
    $("#imgButton").append(img_button)
    buttons++;
    }
  }
  if (fields == 3) {
    document.getElementById("addButton").disabled = true;
  }
}

function removeImage() {
  document.getElementById(fields).remove();
  fields--;
  document.getElementById("addButton").disabled = false;
  if (fields == 1) {
    document.getElementById('removeButton').remove();
    buttons = 0;
  }
}


function post_pack(orderid) {
  if (fields == 1) {
    if (document.getElementById(1).value.length == 0) {
      var orig1 = document.getElementById(1).style.backgroundColor;
      document.getElementById(1).style.backgroundColor = '#ff5252';
      setTimeout(function() {
           document.getElementById(1).style.backgroundColor = orig1;
      }, 1500);
    }
    else {
      pack_call(orderid);
    }
  }

  if (fields == 2) {
    if (document.getElementById(1).value.length == 0) {
      var orig1 = document.getElementById(1).style.backgroundColor;
      document.getElementById(1).style.backgroundColor = '#ff5252';
      setTimeout(function() {
           document.getElementById(1).style.backgroundColor = orig1;
      }, 1500);
    }
    if (document.getElementById(2).value.length == 0) {
      var orig2 = document.getElementById(2).style.backgroundColor;
      document.getElementById(2).style.backgroundColor = '#ff5252';
      setTimeout(function() {
           document.getElementById(2).style.backgroundColor = orig2;
      }, 1500);
    }
    if (document.getElementById(1).value.length != 0 && document.getElementById(2).value.length != 0) {
      pack_call(orderid);
    }
  }

  if (fields == 3) {
    if (document.getElementById(1).value.length == 0) {
      var orig1 = document.getElementById(1).style.backgroundColor;
      document.getElementById(1).style.backgroundColor = '#ff5252';
      setTimeout(function() {
           document.getElementById(1).style.backgroundColor = orig1;
      }, 1500);
    }
    if (document.getElementById(2).value.length == 0) {
      var orig2 = document.getElementById(2).style.backgroundColor;
      document.getElementById(2).style.backgroundColor = '#ff5252';
      setTimeout(function() {
           document.getElementById(2).style.backgroundColor = orig2;
      }, 1500);
    }
    if (document.getElementById(3).value.length == 0) {
      var orig3 = document.getElementById(3).style.backgroundColor;
      document.getElementById(3).style.backgroundColor = '#ff5252';
      setTimeout(function() {
           document.getElementById(3).style.backgroundColor = orig3;
      }, 1500);
    }
    if (document.getElementById(1).value.length != 0 && document.getElementById(2).value.length != 0 && document.getElementById(3).value.length != 0) {
      pack_call(orderid);
    }
  }
}


function pack_call(oid) {
  document.getElementById("packButton").disabled = true;
  document.getElementById("deleteButton").disabled = true;
	document.getElementById("packButton").innerHTML = "<div id='spinner-load' class='spinner-border text-warning'></div>"
  links = [];
  for (var i=1;i<=fields;i++) {
      var inp_val = document.getElementById(i).value;
      links.push(inp_val+"nTnsLRK");
  }
  var joined_links = links.join();
  $.post("/pack_order", {
      img_links: joined_links,
      order_id: oid
  }).done(
  function(response){
      location.replace(response);
   })
   .fail(
   function(response){
      document.getElementById("modalBody").innerHTML = response.responseText;
      $("#myModal").modal('show');
      document.getElementById("packButton").innerHTML = "PACK ORDER";
      document.getElementById("packButton").disabled = false;
      document.getElementById("deleteButton").disabled = false;
    });
}


function deleteButton() {
  document.getElementById("deletion-reason").value = "";
  $("#deleteModal").modal('show');
}


function buttonTroll() {
  document.getElementById("deletion-reason").value = "We don't accept Troll Orders, your name will be added to the blacklist if multiple Troll Orders found on your ID!";
}

function buttonInvalid() {
  document.getElementById("deletion-reason").value = "Sorry the item you've ordered is invalid and we can't accept it, your name will be added to the blacklist if multiple Invalid Orders found on your ID!";
}

function buttonUnreleased() {
  document.getElementById("deletion-reason").value = "Sorry the item you've ordered is currently unreleased and you've to wait until it's official release, your name will be added to the blacklist if multiple Invalid Orders found on your ID!";
}

function buttonDelete(oid) {
  if (document.getElementById("deletion-reason").value.length == 0) {
    var del_val = document.getElementById("deletion-reason").style.backgroundColor;
    document.getElementById("deletion-reason").style.backgroundColor = '#ff5252';
    setTimeout(function() {
         document.getElementById("deletion-reason").style.backgroundColor = del_val;
    }, 1500);
  }
  else {
    document.getElementById("finalDelete").disabled = true;
  	document.getElementById("finalDelete").innerHTML = "<div id='spinner-load' class='spinner-border text-warning'></div>"
    var reason = document.getElementById("deletion-reason").value;
    $.post("/delete_order", {
        deletion_reason: reason,
        order_id: oid
    }).done(
    function(response){
        location.replace(response);
     })
     .fail(
     function(response){
        document.getElementById("modalBody").innerHTML = response.responseText;
        $("#myModal").modal('show');
        document.getElementById("finalDelete").disabled = false;
      	document.getElementById("finalDelete").innerHTML = "DELETE ORDER"
      });
  }
}
