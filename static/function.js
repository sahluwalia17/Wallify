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
  console.log("DRAG: ");
  console.log(dragEvent);

  dragEvent.dataTransfer.setData("Id",    dragEvent.target.id+"|"+dragEvent.target.parentNode.id);
  dragId = dragEvent.target.id;
  //swap box3 & box6
  //dragId = box3
  console.log(dragId);
}

function trackhover(x) {
  // console.log(tracknames[x-1] + " by " + artistnames[x-1] + " in " + albumnames[x-1]);

  var htmlStr = '<ul>';
  htmlStr += '<li class="song">' + tracknames[x-1] + '</li>';
  htmlStr += '<li>' + artistnames[x-1] + '</li>';
  htmlStr += '</ul>';
  // console.log(htmlStr);
  var x = document.getElementsByClassName("album-info");
  for(var i = 0; i<x.length; i++){
    x[i].innerHTML = htmlStr;
  }

}

function trackleave(x) {
  // console.log(tracknames[x-1] + " by " + artistnames[x-1]);
  var box = "box" + String(x);
  var element = document.getElementById(box);
  element.setAttribute("style","filter: contrast(100%);");
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
                  a.href = "./final.jpg";
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
  console.log("DROP data: " + dropData);
  console.log(dropEvent);
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

  // var dropData = dropEvent.dataTransfer.getData("Id");
  // dropItems = dropData.split("|");
  // var prevElem = document.getElementById(dropItems[1]);
  // var swap1 = parseInt(dropEvent.target.id.substring(3));
  // var swap2 = parseInt(dragId.substring(3));
  // var temp = swap1;
  // ints[ints.indexOf(swap1)] = swap2;
  // ints[ints.indexOf(swap2)] = temp;
  // prevElem.getElementsByTagName("div")[0].id = dropEvent.target.id;
  // dropEvent.target.id = dropItems[0];
  // dropEvent.preventDefault();

}

// function drop(ev) {
//   console.log("DROP");
//   ev.preventDefault();
//   var src = document.getElementById(ev.dataTransfer.getData("src"));
//   var srcParent = src.parentNode;
//   var tgt = ev.currentTarget.firstElementChild;

//   ev.currentTarget.replaceChild(src, tgt);
//   srcParent.appendChild(tgt);

//   console.log(tracknames);
// }