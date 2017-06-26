$(document).ready(function () {
    // 以往发布模块的标签效果实现
    var $_clk_li_old = 0;
    $(".post-box-tab").hide().eq($_clk_li_old).show();
    $(".post-box-li").click(function (e) {
        $(this).addClass("active").siblings().removeClass("active");
        e.preventDefault();
        var $_clk_li = $(this).index();
        if ($_clk_li != $_clk_li_old) {
            $(".post-box-tab").slideUp().eq($_clk_li).slideDown()
        }
        $_clk_li_old = $_clk_li;
    });

    // 发布页相关
    $("#st_type").change(function () {
        //alert($(this).val())
    });

});

$(window).scroll(function () {
    // 个人中心的相关设置
    $(".center-left").height($('.center-right').height());
});