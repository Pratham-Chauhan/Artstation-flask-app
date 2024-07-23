
// update image view
function update_image(img) {
    // console.log(img);
    
    $("a.link").attr("href", img); // update download link

    $("#viewer").css({ display: "none" }); // hide the old image

    $("#viewer").attr("src", img); // set the new image link

    // wait for loading the new image
    $("#loading").css({ display: "block" }); // show loading text

    $("#viewer")[0].onload = function () {
        $("#loading").css({ display: "none" });
        $("#viewer").css({ display: "block" });
        update_size();
    };
}
// update image size text
function update_size() {
    var img = $("#viewer")[0];
    // console.log('Image is loaded!')
    // get image size
    // imgH = img.offsetHeight; // height on the screen
    // imgW = img.offsetWidth; // width on the screen

    i_height = img.naturalHeight;
    i_width = img.naturalWidth;

    ratex = (i_width/window.innerWidth).toFixed(1);
    ratey = (i_height/window.innerHeight).toFixed(1);

    $("#size_info").html(`${i_width} x ${i_height}`);
}


if ($("#viewer")[0].complete) {
    update_size();
} 
else {
    $("#viewer")[0].onload = update_size;
}
