imglist = [];  // 目前显示的图片
category_now="all";  // 目前选中的类别
is_draw = "no";       // 是否画了图
pic_n  = 0   //  瀑布流加载图片数量
load_new_img = 50  // 每次加载新的数量

$(window).scroll(function(){
    var scrollTop = $(this).scrollTop();
    var scrollHeight = $(document).height();
    var windowHeight = $(this).height();
    if(scrollTop + windowHeight + 50 > scrollHeight){
        pinterest(imglist, pic_n, imgload, category_now)
        pic_n += load_new_img
    }
});

// 初始化右侧图像显示
function initialize_page(){
    document.getElementById('card-columns').innerHTML="";
    for(var i=0;i<7;i++){
        var contain = document.createElement("div");
        document.getElementById('card-columns').append(contain);
        contain.setAttribute("id","column_"+ i);
        contain.setAttribute("style","width:13%; height:0px;float:left;margin-right:10px");
    }
}

// 瀑布流
function pinterest(imglist, pic_n, callback, category=""){
    for(var i=pic_n; i<(pic_n + load_new_img ); i++){
        let img_url = imglist[i] + Date.parse(new Date());
        let img = new Image();
        img.src = img_url;
        let this_category = category
        console.log(category_now)

        img.onload = function () {
            if (this_category != category_now){return;}
            callback.call(img)
        };
    }
}

function imgload(){
    let img_contain = document.getElementById('card-columns');
    let width = document.getElementById("column_0").offsetWidth
    // let width = document.body.clientWidth * 0.03
    let height = this.height / this.width * width
    let column_n = find_lowest_column()
    let columns = img_contain.getElementsByTagName("div")
    columns[column_n].innerHTML += '<img src=' + this.src + '" style="flow:left; width:' + width + 'px;height:' + height + 'px"' + ' />'
    columns[column_n].style.height = parseInt(columns[column_n].style.height) + height + "px"
    AddImgClickEvent();
}


function find_lowest_column() {
    var img_contain = document.getElementById('card-columns');
    var contain = img_contain.getElementsByTagName("div")
    var index = 0
    var contrast = 99999999999999
    for(var i=0;i<contain.length;i++){
        if(parseInt(contain[i].style.height)<contrast){
            contrast = parseInt(contain[i].style.height)
            index = i
        }
    }
    return index
}

// 点击图片查找相似图片
function AddImgClickEvent(){
    var objs = document.getElementById("card-columns").getElementsByTagName("img")
    for(var i=0;i<objs.length;i++){
        objs[i].onclick=function(){
            var width = this.style.width;
            var height = this.style.height;

            var file_name = this.src;
            var formData = new FormData();
            formData.append("file_name",file_name);
            initialize_page();
            console.log(this.style.width);
            document.getElementById('column_0').innerHTML +='<img id="first" style="flow:left; border:solid 5px red; width:'+width+';height:'+height+';" src=' + file_name +' />'
            lSendUrl('POST', 'http://localhost:12121/click_pic',formData,
                function(response){

                    imglist = response['pic_list'];
                    pic_n = 0;
                    category_now = "click_similar"
                    pinterest(imglist, pic_n, imgload, "click_similar");
                    // for(var i=0;i<response['pic_list'].length;i++){
                    //     document.getElementById('card-columns').innerHTML += '<img src=' + response['pic_list'][i] + '" style="width:6vw;height:6vw"' +' />'
                    // }
                    $("#text").html("Info: The following is a similar infographics of the first infographics");
                }
            )
        }
    }
}

function select_pic(pic_flow) {
    //  清除页面元素
    document.getElementById('card-columns').innerHTML = "";
    var seed_id = "null";
    var pic_flow = pic_flow;
    category_now = pic_flow;
    var vnf_class = document.getElementsByClassName("VNF_Class")
    for (i = 0; i < vnf_class.length; i++) {
        vnf_class[i].style = "border: solid 1px black; width: 12%; height: 12%";
    }
    document.getElementById(pic_flow).style = "border: solid 5px red; width: 12%; height: 12%";
    console.log(pic_flow)
}



//  画图
var canvas_width = document.body.clientWidth * 0.18;
var linewidth = canvas_width * 0.13
var myCanvas = "<canvas id='c1' style='border-style: inset' width='" + canvas_width + "px' height='"+ canvas_width + "px'></vanvas>";
document.getElementById('draw_query').insertAdjacentHTML("beforeBegin", myCanvas);

window.onload = function() {
    var oC = document.getElementById('c1');
    var oCG = oC.getContext('2d');
    oCG.fillStyle = "#FFFFFF";
    oCG.fillRect(0,0,canvas_width,canvas_width);

    oCG.lineWidth=linewidth;
    oC.onmousedown = function(ev) {
        var ev = ev || window.event;
        oCG.moveTo(ev.clientX-oC.offsetLeft,ev.clientY-oC.offsetTop); //ev.clientX-oC.offsetLeft,ev.clientY-oC.offsetTop鼠标在当前画布上X,Y坐标
        document.onmousemove = function(ev) {
            var ev = ev || window.event;//获取event对象
            oCG.lineTo(ev.clientX-oC.offsetLeft,ev.clientY-oC.offsetTop);
            oCG.stroke();
        };
        oC.onmouseup = function() {
            is_draw ="yes";
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
};

// 清除canvas中元素
function clearCanvas(){
    var c=document.getElementById("c1");
    c.width=c.width;
    var c = c.getContext('2d');
    c.fillStyle =  "#FFFFFF";
    c.fillRect(0,0,canvas_width,canvas_width);
    c.lineWidth=linewidth;
    is_draw ="no"
}