var ints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18];
var tokenARR = [];
var dragId;

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(dragEvent) {
  console.log("drag: ");
  console.log(dragEvent);
  dragEvent.dataTransfer.setData("Id", dragEvent.target.id+"|"+dragEvent.target.parentNode.id);
  dragId = dragEvent.target.id;
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
  inswap1 = ints.indexOf(swap1);
  inswap2 = ints.indexOf(swap2);
  ints[inswap1] = swap2;
  ints[inswap2] = temp;
  prevElem.getElementsByTagName("div")[0].id = dropEvent.target.id;
  dropEvent.target.id = dropItems[0];
  dropEvent.preventDefault();
}
