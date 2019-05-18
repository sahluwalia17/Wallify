var ints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18];
var tokenARR = [];
var dragId;

function init()
{
  var token = Math.floor((Math.random() * 1000) + 1);
  console.log(token);
  window.alert(token);
  tokenARR.push(token);
  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    url: "/receive_token",
    traditional: "true",
    data: JSON.stringify({tokenARR}),
    dataType: "json"
    });
}

function allowDrop(ev) {
  ev.preventDefault();
}
function drag(dragEvent) {
  dragEvent.dataTransfer.setData("Id",    dragEvent.target.id+"|"+dragEvent.target.parentNode.id);
  dragId = dragEvent.target.id;
}
function download() {
        $.ajax({
          type: "POST",
          contentType: "application/json;charset=utf-8",
          url: "/receive",
          traditional: "true",
          data: JSON.stringify({ints}),
          dataType: "json",
          cache: false
          });

          var a = document.createElement('a');
          a.href = "./final.jpg";
          a.download = "final.jpg";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
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
