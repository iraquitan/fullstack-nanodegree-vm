$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});

//$('.signup-js').click(function(){
//    $.ajax({
//            url: '/signup',
//            type: "POST",
//            dataType: 'json',
//            success: function(data) {
//                if (data.status == 'ok') { //if your response have 'status' key
//                   alert('Logged');
//                } else {
//                   alert('Error.');
//                }
//            }
//        });
//})