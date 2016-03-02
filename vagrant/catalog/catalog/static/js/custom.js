// Used to activate nav bar items on click
$(".nav li.active a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});