var imgX, imgY, imgH, imgW;
var count = 0;

function mouse_away_from_image_center(mouseX, mouseY) {
    // calculate distance between mouse pointer and image center
    imgX = $("#viewer")[0].offsetLeft;
    imgY = $("#viewer")[0].offsetTop;

    imgH = $("#viewer")[0].offsetHeight;
    imgW = $("#viewer")[0].offsetWidth;

    deltaY = mouseY - (imgY + imgH / 2);
    deltaX = imgX + imgW / 2 - mouseX;
    console.log("delta X Y:", deltaX, deltaY);

    // return [deltaX, deltaY];
}

function move_image_to_center() {
    // get image position
    imgX = $("#viewer")[0].offsetLeft;
    imgY = $("#viewer")[0].offsetTop;

    imgH = $("#viewer")[0].offsetHeight;
    imgW = $("#viewer")[0].offsetWidth;

    console.log("Intial x y:", imgX, imgY);

    // distance between the image center and the screen center coordinates
    var dx = imgX + imgW / 2 - centerX;
    var dy = imgY + imgH / 2 - centerY;

    console.log("dx:", dx);
    console.log("dy:", dy);

    var x2 = imgX - dx;
    var y2 = imgY - dy;

    console.log("final x:", x2, "screen center:", centerX, x2 + imgW / 2);
    console.log("final y:", y2, "screen center:", centerY, y2 + imgH / 2);

    // return [x2 + 0.2* deltaX, y2 - 0.5 *deltaY]
    return [x2, y2];
    // return [0,0]
}

// scroll horizontally to middle of the viewer    
function scrollToMiddle(element) {
    const scrollLeft = (element.scrollWidth - element.clientWidth) / 2;

    element.scrollTo({
        left: scrollLeft,
        behavior: 'smooth'
    });
}


function hide_menu() {
    $("#viewer").css({ width: "auto", border: "none" }); //  reset the image size and remove the border
    window.scrollTo(0, 0);

    // hide the above panel
    $(".menu").css({ display: "none" });
    $(".menu2").css({ display: "none" });
}

function fullview(event) {
    var mouseX = event.clientX;
    var mouseY = event.clientY;

    console.log(mouseX, mouseY);

    // mouse_away_from_image_center(mouseX, mouseY)
    // var deltaY, deltaX;

    // show or hide the viewer
    if (count == 0) {
        // full view
        count = 1;

        hide_menu();

        document.body.style.backgroundColor = "#242424"; // dark

        if (device_type == "desktop") {
            // show the image relocation animation
            const element = document.getElementById("viewer");
            initial_pos = calculate_image_position(mouseX, mouseY);
            middle_pos = move_image_to_center();
            init_x = initial_pos[0];
            init_y = initial_pos[1];

            element.animate(
                [
                    {
                        left: middle_pos[0] + "px",
                        top: middle_pos[1] + "px",
                    }, // starting position
                    { left: init_x + "px", top: init_y + "px" }, // ending position
                ],
                {
                    duration: 400, // 0.7 seconds
                    easing: "ease-out",
                    fill: "backwards",
                }
            );

            // jquery version
            // $("#viewer").animate(
            // {
            //     left: -500 +'px' ,
            //     top: -500 + 'px'
            // }, // ending position
            // {
            //     duration: 700, // 0.7 seconds
            //     // easing: "ease-out",
            // }
            // );

            $("#viewer").css({ left: init_x + "px", top: init_y + "px" });

            // disable scrolling, not recommended right now as floating mode is not perfect.
            $('body').css({ overflow: 'hidden' });
        } else {
            // mobile
            // margin: auto is the cause of all the miscalculations and image position,
            // cause it change the left and top properties of the image and center the image.
            $("#viewer").css({ margin: "auto" });
            
            var container = document.getElementById("wrapper");
            scrollToMiddle(container)
            

        }
    } else {
        // normal view
        count = 0;

        $("#viewer").css({
            width: "100%",
            border: "3px groove #ccc",
            left: 0 + "px",
            top: 0 + "px",
        });

        // show above panel
        document.body.style.backgroundColor = "hsl(0 0% 93% / 1)"; // light
        $(".menu").css({ display: "flex" });
        $(".menu2").css({ display: "flex" });

        $("body").css({ overflow: "auto" });
    }
}
