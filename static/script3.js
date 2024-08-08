
// update image view
function updateImg(index) {
    console.log(index);
    currentIndex = index;

    $("a.link").attr("href", images[index].src); // update download link

    $("#viewer").css({ display: "none" }); // hide the old image

    $("#viewer").attr("src", images[index].src); // set the new image link

    // wait for loading the new image
    $("#loading").css({ display: "block" }); // show loading text

    $("#viewer")[0].onload = function () {
        $("#loading").css({ display: "none" });
        $("#viewer").css({ display: "block" });
        updateSize();
    };

    $(".indicator").removeClass("active");
    $(`.indicator[data-index=${index}]`).addClass("active");
}
// update image size text
function updateSize() {
    var img = $("#viewer")[0];
    // console.log('Image is loaded!')
    // get image size
    // imgH = img.offsetHeight; // height on the screen
    // imgW = img.offsetWidth; // width on the screen

    i_height = img.naturalHeight;
    i_width = img.naturalWidth;

    ratex = (i_width / window.innerWidth).toFixed(1);
    ratey = (i_height / window.innerHeight).toFixed(1);

    $("#size_info").html(`${i_width} x ${i_height}`);
}

if ($("#viewer")[0].complete) {
    updateSize();
} else {
    $("#viewer")[0].onload = updateSize;
}

// indicator menu
$.each(imageUrls, function (index) {
    // const button = $('<button class="button">').text(`${index}`)
    const indicator = $('<div class="indicator">').attr("data-index", index);
    indicator.click(() => updateImg(index));

    $(".menu").append(indicator);
});

var currentIndex = 0;
updateImg(currentIndex); // show the first image

function goToNextImage() {
    updateImg((currentIndex + 1) % imageUrls.length);
}
function goToPrevImage() {
    updateImg((currentIndex - 1 + imageUrls.length) % imageUrls.length);
}
// Event Listeners -- Interactive
document.addEventListener("click", (event) => {
    const width = window.innerWidth;
    const clickPosition = event.clientX;

    var threshold = window.innerWidth * 0.1; // 10% of the window width
    if (device_type == "mobile") {
        threshold = window.innerWidth * 0.16; // 20% of the window width (mobile)
    }
    console.log("Clicked on", event.target.id, clickPosition, width);

    if (clickPosition < threshold) {// Clicked on the left side
        goToPrevImage();
    } else if (clickPosition > window.innerWidth - threshold) {// Clicked on the right side
        goToNextImage();

    } else {
        console.log("clicked in between screen.");
        if (event.target.id == "viewer") {
            fullview(event);
        }
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
        goToPrevImage();
    } else if (event.key === "ArrowRight") {
        goToNextImage();
    }
});

// HD mode
let hdMode = false;
document.addEventListener("contextmenu", (event) => {
    if (event.target.id == "viewer") {
        event.preventDefault(); // Prevent the default context menu from appearing
        const img = event.target;
        const largeSrc = img.src.replace("/4k/", "/large/");
        const hdSrc = img.src.replace("/large/", "/4k/");

        if (hdMode) {
            event.target.src = largeSrc;
        } else {
            event.target.src = hdSrc;
        }

        hdMode = !hdMode;
    }
});

window.addEventListener('wheel', (event) => {
    if (fullMode) {
        if (event.deltaY < 0) { // Scrolling up
            goToNextImage();

        } else if (event.deltaY > 0) { // Scrolling down
            goToPrevImage();
        }
    }
});