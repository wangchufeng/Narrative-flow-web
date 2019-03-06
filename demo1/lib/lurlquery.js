lSendUrl = function(PostType, Url, formData, successPaperState, self){
    var xmlhttp;

    if(PostType == "GET"){
        if(window.XMLHttpRequest){
            xmlhttp = new XMLHttpRequest();
        }
        else{
            xmlhttp = new ActiveXObject("Microsoft.XMLHttpRequest");
        }
        xmlhttp.open(PostType, Url, true);
        xmlhttp.onreadystatechange = function(){
            successPaperState();
        }

        xmlhttp.send(null)
    }
    else{
        $.ajax({
            url: Url,
            type: "POST",
            dataType: "JSON",
            data: formData,
            crossDomain: true,
            processData: false,
            contentType: false,
            success: function(response){
                // console.log("response",response);
                successPaperState(response, self);
            },
            error: function(jqXHR, textStatus, errorMessage){
                console.log("errorMessage",errorMessage);
            }
        });
    }
}