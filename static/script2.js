var centerX = window.innerWidth / 2; // Center X coordinate
var centerY = window.innerHeight / 2; // Center Y coordinate
var ratex, ratey;
var i_height, i_width;

function calculate_image_position(mouseX, mouseY) {
    // var img = $("#viewer")[0];

    // const ratex = 0.8;
    // const ratey = 1.5;

    // OG and simple calculation
    var xx = centerX - (i_width / 2) + ratex * (centerX - mouseX); // Calculate X position
    // // const xx = centerX + 1 * (mouseX - centerX) - imgW / 2;
    var yy = centerY - (i_height / 2) + ratey * (centerY - mouseY); // Calculate Y position

    return [xx, yy];

    // account for image positon

    // const offsetX = mouseX - imgX;
    // const offsetY = mouseY - imgY;

    // account for scroll
    // const scrollX = window.pageXOffset;
    // const scrollY = window.pageYOffset;
    
    // Get image position and size
    imgX = $("#viewer")[0].offsetLeft;
    imgY = $("#viewer")[0].offsetTop;
    imgH = $("#viewer")[0].offsetHeight;
    imgW = $("#viewer")[0].offsetWidth;


    // Calculate distance between image center and screen center
    dx = ((imgX + imgW / 2) - centerX);
    dy = ((imgY + imgH / 2) - centerY);

    // Calculate new image position to center it on the screen
    x2 = centerX - (i_width / 2);
    y2 = centerY - (i_height / 2);

    // Adjust Y position based on mouse position
    yy = y2 + (centerY - mouseY);
    xx = x2 + (centerX - mouseX);

    // console.log('New image position:', x2, yy);
    return [xx, yy];
}

// Function to check media query
function checkMediaQuery() {
    const mediaQuery = window.matchMedia("(max-width: 900px)");

    // Initial check
    if (mediaQuery.matches) {
        console.log("Oh no!  It's a mobile device");
        // alert("Oh no! It's a mobile device");
        return "mobile";
    } else {
        console.log("Yippee! It's a desktop device");
        return "desktop";
    }
}
var device_type = checkMediaQuery();
var loc;

if (device_type == "desktop") { // add mouse move listener
    document.addEventListener("mousemove", (e) => {
        const mouseX = e.clientX;
        const mouseY = e.clientY;

        if (fullMode) {
            // console.log("in floating mode.");
            // console.log(x, y);
            loc = calculate_image_position(mouseX, mouseY);
            // console.log(loc[0], loc[1]);
            $("#viewer").css({
                left: loc[0] + "px",
                top: loc[1] + "px",
            });
        }
    });
}
