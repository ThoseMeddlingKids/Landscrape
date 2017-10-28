$(".add").click(function(){
  $("form>p:first-child").clone(true).inserBefore("form > p:last-child");
  return false;
});

$(".remove").click(function(){
  $(this).parent().remove();
});
