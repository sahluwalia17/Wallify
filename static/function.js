var ints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18];
var tokenARR = [];
var dragId;
var tracknames = []
var artistnames = []

function populate(trackdata) {
    var jsonstring = JSON.stringify(trackdata);
    var json = JSON.parse(jsonstring);
    for (var key in json) {
      tracknames.push(key);
      artistnames.push(json[key]);
    }
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(dragEvent) {
  dragEvent.dataTransfer.setData("Id",    dragEvent.target.id+"|"+dragEvent.target.parentNode.id);
  dragId = dragEvent.target.id;
}

function trackhover(x) {
  console.log(tracknames[x-1] + " by " + artistnames[x-1]);

  var htmlStr = '<ul>';
  htmlStr += '<li class="song">' + tracknames[x-1] + '</li>';
  htmlStr += '<li>' + artistnames[x-1] + '</li>';
  htmlStr += '</ul>';
  console.log(htmlStr);
  var x = document.getElementsByClassName("album-info");
  for(var i = 0; i<x.length; i++){
    x[i].innerHTML = htmlStr;
  }

}

function trackleave(x) {
  console.log(tracknames[x-1] + " by " + artistnames[x-1]);
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
  dropItems = dropData.split("|");
  var prevElem = document.getElementById(dropItems[1]);
  var swap1 = parseInt(dropEvent.target.id.substring(3));
  var swap2 = parseInt(dragId.substring(3));
  var temp = swap1;
  ints[ints.indexOf(swap1)] = swap2;
  ints[ints.indexOf(swap2)] = temp;
  prevElem.getElementsByTagName("div")[0].id = dropEvent.target.id;
  dropEvent.target.id = dropItems[0];
  dropEvent.preventDefault();
}
