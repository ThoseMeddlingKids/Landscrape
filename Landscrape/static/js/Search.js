var counter = 1;
var limit = 8;
function addInput(divName){
  if (counter == limit){
    alert("You may only Search for 8 Things at a Time!")
  }
  else{
    var newDiv = document.createElement('div');
    newDiv.innerHTML = "{{render_field(form.searchquery, class = "form-control")}}";
    document.getElementByID(divName).appendChild(newDiv);
    counter++;
  }
}
