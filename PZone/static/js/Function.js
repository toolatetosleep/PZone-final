//动态设置导航的高度
var $_com_on_load = true;
var $_aside = $("aside").height();

$(document).ready(function () {

    //功能性JS支持
    $('.disabled-btn-hover').hover(function () {
        $(this).removeClass('disabled-btn-hover');
    }, function () {
        $(this).addClass('disabled-btn-hover');
    });
    $(".hover-button").hover(function () {
        $(this).removeClass('hover-button-off').addClass('hover-button-on');
    }, function () {
        $(this).removeClass('hover-button-on').addClass('hover-button-off');
    });

    //Mask 设置
    $('#mask').click(function () {
        Pop_box_hide();
    });
    $('#mask1').click(function () {
        Pop_box_hide1();
    });
    $('.pop-box').click(function (e) {
        e.stopPropagation();
    });

    //登录/注册框
    $('#login_form').bind("submit", function (e) {
        e.preventDefault();
        if (onlogin()) {
            login_form.submit();
        }
    })

});

//登录/注册框
function onlogin() {
    var $name = $('#id_username');
    var $pwd = $('#id_password');
    var username = $name.val().trim();
    var password = $pwd.val().trim();
    var reg = /^.*[~!@#\$%\^&\*\(\)_+\-=\[\]\{\}\\\|\'\";:,\<\.\>\/\?\s+].*$/;
    if (username.length < 6 || username.length > 16 || reg.test(username)) {
        GetRed($name);
    } else {
        GetBack($name);
    }
    if (password.length < 6 || password.length > 16) {
        GetRed($pwd);
    } else {
        GetBack($pwd);
    }
    if (username.length <= 0 && password <= 0) {
        btnSetText("用户名和密码不能为空");
        return false;
    } else if (username.length <= 0) {
        btnSetText("用户名不能为空");
        return false;
    } else if (username.length < 6) {
        btnSetText("用户名不能小于6个字符");
        return false;
    } else if (username.length > 16) {
        btnSetText("用户名不能大于16个字符");
        return false;
    } else if (reg.test(username)) {
        btnSetText("用户名不能包含特殊符号");
        return false;
    } else if (password.length <= 0) {
        btnSetText("密码不能为空");
        return false;
    } else if (password.length < 6) {
        btnSetText("密码不能小于6个字符");
        return false;
    } else if (password.length > 16) {
        btnSetText("密码不能大于16个字符");
        return false;
    } else {
        btnSetText("确定");
        ajaxUserCheck();
    }
}
function ajaxUserCheck() {
    var username = $('#id_username').val().trim();
    var password = $('#id_password').val().trim();
    var url = $('#ajax_user_url').val();
    $.ajax({
        cache: true,
        type: "POST",
        url: url,
        data: {'username': username, 'password': password},
        async: false,
        success: function (data) {
            if (parseInt(data) == 1) {
                btnSetText("登录成功");
                login_form.submit();
                return true;
            } else if (parseInt(data) == 0) {
                btnSetText("密码有误，请重试");
                return false;
            }
        },
        error: function () {
            btnSetText("似乎出了点小问题，请稍后重试");
            return false;
        }
    });
}
function btnSetText(str) {
    $('#id_button').text(str);
}
function GetRed(obj) {
    $(obj).css("border-bottom-color", "red");
}
function GetBack(obj) {
    $(obj).css("border-bottom-color", "#11c7eb");
}

//评论区在可视范围内加载
function on_sight_load() {
    var com_sec = $("#com_section");
    var mainOffsetTop = com_sec.offset().top;
    var mainHeight = com_sec.height();
    var winHeight = $(window).height();
    $(window).scroll(function () {
        var winScrollTop = $(window).scrollTop();
        if (winScrollTop > mainOffsetTop + mainHeight || winScrollTop < mainOffsetTop - winHeight) {

        } else {
            if ($_com_on_load) {
                load_com(com_sec);
                $_com_on_load = false;
            }
        }
    })
}

//更新评论区内容（换页）
function update_com(url) {
    var $_block = $('.letter-box-container');
    //$_block.each(function () {
    //    $(this).slideUp(500)
    //});
    $_block.remove();
    var com_sec = $("#com_section");
    com_sec.attr('data', url);
    load_com(com_sec);
    com_top();
}

//获取评论区内容
function load_com(com_sec) {
    var url = com_sec.attr('data')
    $.ajax({
        cache: true,
        type: "POST",
        url: url,
        data: {},
        async: false,
        success: function (data) {
            add_com(data)
        }
    });
}

//获取评论
function add_com(data) {
    var $id = $('#user_id').val();
    var len = 0;
    $.each(data, function (i, data) {
        len += 1;
    })
    $.each(data, function (i, data) {
        var $_html = "<div class='letter-box-container'>";
        $_html += "<div class='letter-box'><div class='letter-boxs letter-box-left'><img src='";
        $_html += data['c_ava'];//用户头像
        $_html += "'/></div><div class='letter-boxs letter-box-right'><div class=";
        $_html += "'letter-box-right-top letter-box-right-top-left'><a href='";
        $_html += data['user_link'];//用户名链接
        $_html += "' class='letter-box-a'>";
        $_html += data['c_name'];//用户名
        $_html += "</a></div><div class='letter-box-right-top letter-box-right-top-right'><a href='";
        $_html += "##";
        $_html += "' class='letter-box-a'>";
        $_html += data['c_time'];//日期
        $_html += "&nbsp;&nbsp;&nbsp;&nbsp;";
        //$_html += data['c_flt'];//楼层
        $_html += "</a></div><div class='letter-box-right-mid'><p class='letter-box-p'>";
        $_html += data['c_con'];//内容
        $_html += "</p></div><div class='letter-box-right-btm'>"
        if (parseInt($id) == parseInt(data['c_id'])) {
            $_html += "<a onclick='page_href_com(";
            $_html += parseInt(data['c_com_id']);//删除
            $_html += ")' style='cursor: pointer' class='letter-box-a'>删除</a>";
        }
        $_html += "<a data='";
        $_html += data['com_link'];
        $_html += "' style='cursor: pointer;' onclick='";
        $_html += "fetch_com_com(";//看回复的链接
        $_html += data['c_com_id'] + ", ";
        $_html += data['c_id'] + ", \"";
        $_html += data['c_name'] + "\", this)";
        $_html += "' class='letter-box-a'>回复(";
        $_html += data['c_rep'];//回复
        $_html += ")</a></div></div></div></div>";
        $('#give-com').after($_html);
        if (i == len - 1) {
            $_page_this = parseInt(data['page_this']);
            $_page_all = parseInt(data['page_all']);
            pagination();
        }
    });
}

//获取评论的评论
var $_com_id = 0;
function fetch_com_com(id, uid, uname, obj) {
    if ($_com_id == parseInt(id)) {
        $('.com_children').slideToggle();
        return false;
    }
    $_com_id = parseInt(id);
    var $obj = $(obj);
    var $url = $obj.attr('data')
    $('.com_children').slideUp();
    $.ajax({
        cache: true,
        type: "POST",
        url: $url,
        data: {},
        async: false,
        success: function (data) {
            var a = "<div class='letter-box com_children' style='height: 30px;'><div class='letter-boxs " +
                "letter-box-left'></div><div class='letter-boxs letter-box-right'><div class='letter-box-fill' " +
                "style='height: 30px;text-align: center;'><a data='" + uname + "' href='##' onclick='reply_com(" + id.toString() + ", " +
                uid.toString() + ", this)' class='letter-box-a' style='border-radius: " +
                "5px;width: 100%;margin: 5px;display: inline-block;padding: 2px 20px;'>我也说一句</a></div></div></div>";

            $(obj).parent().parent().parent().after(a);

            $.each(data, function (i, data) {
                var $_html = "";
                $_html += "<div class='letter-box com_children'><div class='letter-boxs letter-box-left'></div>";
                $_html += "<div class='letter-boxs letter-box-right'><div class='letter-box-fill'>";
                $_html += "<div class='letter-boxs letter-box-left letter-box-left-sm'><img src='";
                $_html += data['c_ava'];  // 头像地址
                $_html += "' /></div><div class='letter-boxs letter-box-right'><div class='letter-box-right-top letter-box-right-top-left'><a href='";
                $_html += data['glink'];  // 用户链接
                $_html += "' class='letter-box-a'>";
                $_html += data['c_uid'];  // 用户名字
                $_html += "</a><span>回复</span><a href='";
                $_html += data['rlink'];  // 用户链接
                $_html += "' class='letter-box-a'>";
                $_html += data['c_rid'];  // 用户名字
                $_html += "</a></div><div class='letter-box-right-top letter-box-right-top-right'><a class='letter-box-a'>";
                $_html += data['c_time'];  // 时间
                $_html += "</a></div><div class='letter-box-right-mid-sm'><p class='letter-box-p'>";
                $_html += data['c_con'];  // 内容
                $_html += "</p></div><div class='letter-box-right-btm'><a href='";
                $_html += "##";  // 删除链接
                $_html += "' class='letter-box-a'>删除</a><a data='" + data['c_uid'] + "' href='##' onclick='";
                $_html += "reply_com(" + id.toString() + ", " + data['u_give'] + ", this)";  // 回复链接
                $_html += "' class='letter-box-a'>回复</a></div></div></div></div></div>";
                $(obj).parent().parent().parent().after($_html);
            });
        }
    });
}

//回复评论
var $rep_span = "";
function reply_com(cid, uid, obj) {
    if (getCookie("username") != null) {
        setCookie("name", uid.toString());
        setCookie("rev", cid.toString());
        var name = $(obj).attr("data");
        editor.clear();
        var str = "回复 " + name + "：";
        $rep_span = str;
        editor.$txt.html("<p>" + str);
        editor.$txt.blur();
        com_top();
    } else {
        var $html = "<div id='mask'><div class='pop-box'><div class='card'>" +
            "<div class='card-content'><label class='pop-box-input'>" +
            "回复评论请先登录！</label><button class='button pop-box-button' " +
            "style='width: 30%;' onclick='Pop_box_hide()'>确定</button>" +
            "</div></div></div></div>";
        $('body').prepend($html);
        Pop_box_show();
    }
}

// 获取Cookies
function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)"); //正则匹配
    if (arr = document.cookie.match(reg)) {
        return unescape(arr[2]);
    }
    else {
        return null;
    }
}
// 设置Cookies
function setCookie(name, value) {
    document.cookie = name + '=' + escape(value);
}
// 删除Cookies
function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null) {
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
    }
}

//回到评论区上方
function com_top() {
    var top = $('#com_section').offset().top;
    $('body,html').animate({
        scrollTop: top
    }, 500);
}

//Pop-Box 加载及关闭动画
function Pop_box_show() {
    $('#mask').fadeIn(500);
    $('.pop-box').fadeTo(600, 1).animate({
        height: "275px"
    }, 300, 'swing');
}
function Pop_box_show1() {
    //var csrf = $('#login_form').children().first().attr("value");
    //var $html = '<div id="mask">' + $('.reg-form-user-mark').html() + '</div>';
    //$('body').prepend($html);
    $('#mask1').fadeIn(500);
    $('.pop-box').fadeTo(600, 1).animate({
        height: "275px"
    }, 300, 'swing');
    //Mask 设置
    //$('#mask').unbind("click").click(function () {
    //    Pop_box_hide();
    //});
    //$('.pop-box').unbind("click").click(function (e) {
    //    e.stopPropagation();
    //});
}
function Pop_box_hide1() {
    $('.pop-box').animate({
        height: "0px"
    }, 200, 'swing');
    $('#mask1').fadeTo(600, 1).fadeOut(500);
}
function Pop_box_hide() {
    $('.pop-box').animate({
        height: "0px"
    }, 200, 'swing');
    $('#mask').fadeTo(600, 1).fadeOut(500);
}

//页面加载时上方的动画横条
function bar1_loop() {
    var bar = $('.bar1');
    bar.animate({
        width: "50%",
        left: "50%"
    }, 1000, 'swing');
    bar.animate({
        width: "0%",
        left: "100%"
    }, 700, 'linear');
    bar.animate({
        width: "0%",
        left: "0%"
    }, 1, 'linear');
}
