$(".sidebar-dropdown > a").click(function() {// this mounted using for admin panel
    $(".sidebar-submenu").slideUp(200);
    if($(this).parent().hasClass("active")){
        $(".sidebar-dropdown").removeClass("active");
        $(this).parent().removeClass("active");
    }else {
        $(".sidebar-dropdown").removeClass("active");
        $(this).next(".sidebar-submenu").slideDown(200);
        $(this).parent().addClass("active");
    }
});

$("#close-sidebar").click(function() {
    $(".page-wrapper").toggleClass("toggled");
});
$("#show-sidebar").click(function() {
    $(".page-wrapper").addClass("toggled");
});