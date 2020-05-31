var ints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18];
var tokenARR = [];
var dragId;
var urls = []
var albumnames = []
var tracknames = []
var artistnames = []

function populate(trackdata) {
    var jsonstring = JSON.stringify(trackdata);
    var json = JSON.parse(jsonstring);
    for (var key in json) {
      urls.push(key);
      var information = json[key];
      artistnames.push(information[0]);
      tracknames.push(information[1]);
      albumnames.push(information[2]);
    }
    //key is the track id; for exact url append https://open.spotify.com/track/{trackid}
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(dragEvent) {
  dragEvent.dataTransfer.setData("Id",    dragEvent.target.id+"|"+dragEvent.target.parentNode.id);
  dragId = dragEvent.target.id;
}

function trackhover(x) {
  var static = document.getElementsByClassName("static");
  static[0].style.display = "none";

  var songStr = tracknames[x-1] + " by " + artistnames[x-1] + " in " + albumnames[x-1];

  var dynamic = document.getElementsByClassName("dynamic");
  dynamic[0].innerHTML = songStr;
  dynamic[0].style.display = "";
}

function trackleave(x) {
  var static = document.getElementsByClassName("static");
  static[0].style.display="";

  var dynamic = document.getElementsByClassName("dynamic");
  dynamic[0].innerHTML = "";
  dynamic[0].style.display = "none";


}

function download() {
        var token;
        $.ajax({
          type: "POST",
          contentType: "application/json;charset=utf-8",
          url: "/receive",
          traditional: "true",
          data: JSON.stringify({ints}),
          dataType: "json",
          cache: false,
          success : function (response)
              {
                  token = response.toString();
                  var a = document.createElement('a');
                  a.href = "../final.jpg";
                  a.download = "final.jpg";
                  document.body.appendChild(a);
                  a.click();
                  document.body.removeChild(a);
              }
          });

          while(token == null)
          {
            sleep(1000);
          }
}

function drop(dropEvent) {
  var dropData = dropEvent.dataTransfer.getData("Id");
  dropItems = dropData.split("|");
  var prevElem = document.getElementById(dropItems[1]);
  var swap1 = parseInt(dropEvent.target.id.substring(3));
  var swap2 = parseInt(dragId.substring(3));
  var in1 = ints.indexOf(swap1);
  var in2 = ints.indexOf(swap2);

  var tempimg = swap1;
  var temptrack = tracknames[in1];
  var tempart = artistnames[in1];
  var tempalb = albumnames[in1];

  ints[in1] = swap2;
  ints[in2] = tempimg;
  tracknames[in1] = tracknames[in2];
  tracknames[in2] = temptrack;
  artistnames[in1] = artistnames[in2];
  artistnames[in2] = tempart;
  albumnames[in1] = albumnames[in2];
  albumnames[in2] = tempalb;

  prevElem.getElementsByTagName("div")[0].id = dropEvent.target.id;
  dropEvent.target.id = dropItems[0];
  dropEvent.preventDefault();

}
