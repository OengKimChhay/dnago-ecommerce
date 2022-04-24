$(document).ready(function(){

    //--------------------- for dashboard ---------------------------
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

    // ---------------------------- make active dropdown------------------------
    var current = location.pathname;
    $('.sidebar-menu sidebar-dropdown > a').each(function(){
        var $this = $(this);
        // if the current path is like this link, make it active
        if($this.attr('href').indexOf(current) !== -1){
            $this.addClass('active');
        }
        $this.addClass('active');
    })

});