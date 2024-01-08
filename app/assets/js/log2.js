
function myFunction(){
  var x = document.getElementById("selected_email").value;
  //alert(x)
  document.getElementById("user_email").value = x;

  //populate AJAX drop downlist to show car for selected email
  getClubs(x)

  var y = document.getElementById("selected_club").value;
  document.getElementById("club").value = y;

}//end of myFunction

function getClubs(aEmail){
  $.ajax({
      url: "/getClubs", //route in app.py
      type: "POST",
      data: {
          aEmail: aEmail
      },
      error: function(){
          alert("Error");
      }, //end of error
      success: function(data, status, xhr){
          var club_list=[];
          for (var label of data.myClubs){ 
              club_list.push(label)
          }
          populate("#selected_club",club_list)

      } //end of success
  }) //end of ajax call
}// end of getClubs

function populate(selector, club_list){
  
  $(selector).empty();
  $(selector).append("<option value=\"\">Select One Club (by label)</option>");

  if (club_list.length != 0) {
      for (var i=0; i<club_list.length; i++) {
          let select_str = "<option value=\"" + club_list[i] + "\">" + club_list[i] + "</option>";
          $(selector).append(select_str);
      }
  }
}//end of populate
