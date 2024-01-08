class InvalidDataError extends Error {
  constructor(message) {
    super(message);
    this.name = "MyException";
  }
}

function calculateDistance() {
  let swing_speed = document.querySelector("#swing_speed_input").value;
  let distance = document.querySelector("#distance_input").value;

  if (document.querySelector(".output_space > p").innerHTML == "The Output Area") {
    document.querySelector(".output_space > p").innerHTML = "";
  }
  $.ajax({
    url: "/process",
    type: "POST",
    data: { swing_speed: swing_speed, distance: distance },
    success: function(data, status, xhr) {
      console.log(data.clubs);

      if (data.clubs == null) {
        document.querySelector(".output_space > p").innerHTML += "<br><b>Speed = " + swing_speed + " mph, distance = " + distance + " yards</b><br>No golfset recorded yet!<br>";
      } else {var club_list = [];
        for (var club of data.clubs) {
          club_list.push(club)
        }
        if (club_list.length != 0) {
          document.querySelector(".output_space > p").innerHTML += "<br><b>Speed = " + swing_speed + " mph, distance = " + distance + " yards</b><br>";
          for (var oneclub of club_list) {
            document.querySelector(".output_space > p").innerHTML += oneclub[0] + " length = " + oneclub[1] + " loft = " + oneclub[2] +"<br>";
          }
        } else if (club_list.length == 0 ) {
          document.querySelector(".output_space > p").innerHTML += "<br><b>Speed = " + swing_speed + " mph, distance = " + distance + " yards</b><br>No suitable club<br>";
        } 
      }
    },
    error: function(error) {
      document.querySelector(".output_space > p").innerHTML += "Error: " + error.statusText;
    }
  });
  }

  function reset(){
    debugger
    document.querySelector(".output_space > p").innerHTML = "<b>Club Advice</b>";

  let inSwingSpeed = document.querySelector("#swing_speed_input");
  inSwingSpeed.value=""

  let inDistance = document.querySelector("#distance_input"); 
  inDistance.value=""
  }

if(document.getElementById("submit") != null){
  document.querySelector("#submit").addEventListener("click", calculateDistance);
}
if(document.getElementById("reset") != null){
  document.querySelector("#reset").addEventListener("click", reset);
}
