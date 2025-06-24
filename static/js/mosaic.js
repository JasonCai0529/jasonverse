let originalURL = '';
let mosaicURL = '';
let showMosaic = true;

let rotation = 0; // degrees
document.getElementById("rotate-btn").addEventListener("click", () => {
    rotation = (rotation + 90) % 360;
    document.getElementById("mosaic-img").style.transform = `rotate(${rotation}deg)`;

    const imgDiv = document.getElementById("output-img");
    if (rotation == 90 || rotation == 270) { // when the image is in portrait mode
        imgDiv.style.height = "100%";
    } else {
        imgDiv.style.height = "70vh";
    }
});

// a rotate feature && and image loadign in progress animate
document.getElementById("upload-form").addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    let numTiles = formData.get("num_tiles");
    let pixelsPerTile = formData.get("pixels_per_tile");
    // Use default if the field is empty or null
    if (!numTiles) numTiles = 40;
    if (!pixelsPerTile) pixelsPerTile = 50;
    formData.set("num_tiles", numTiles);
    formData.set("pixels_per_tile", pixelsPerTile);


    const res = await fetch('/generate', {
        method: "POST",
        body: formData
    });

    if (!res.ok) {
        // if did not get a valid response
        document.getElementById('output-img').innerHTML =
        `<div class="toast hide">Failed to Generate Moasics
            <p>Please try lowering the number of -Pixels per tile- or -Number of tiles-</p>
        </div>`;
        return;
    }

    const blob = await res.blob();
    const imgURL = URL.createObjectURL(blob);
    mosaicURL = imgURL;
    document.getElementById("mosaic-img").src = imgURL; // set up the mosiac picture
    
    // get the resize original img and store them in original url
    const resOriginal = await fetch('/getOriginal');
    const blobOriginal = await resOriginal.blob();
    originalURL = URL.createObjectURL(blobOriginal);


    // bring up the operation buttons regard to the output image
    document.getElementById("rescale-section").style.display = "block";
    document.getElementById('reset-btns-container').style.display = "block";
    const saveBtn = document.getElementById("save-btn");
    saveBtn.style.display = "inline-block";
    saveBtn.onclick = ()=> {
        const a = document.createElement('a');
        a.href = imgURL;
        a.download = 'mosaic.png';
        a.click();
    }
});


document.getElementById("upload-form").addEventListener('change', ()=> {
    if (document.getElementById('mosaic-img').src) {
        document.getElementById('generate-btn').innerHTML = "Regenerate";
    }
});


document.getElementById('output-img').addEventListener('click', ()=> {
    const mosaicImg = document.getElementById("mosaic-img");
    if (showMosaic) {
        mosaicImg.src = originalURL;
    } else {
        mosaicImg.src = mosaicURL;
    }
    showMosaic = !showMosaic;
});

document.getElementById("clear-btn").addEventListener('click', ()=> {
      location.reload();
});

document.getElementById("clear-img-btn").addEventListener('click', ()=> {
    document.getElementById('output-img').innerHTML = '';
});


const scaleSlider = document.getElementById("scale-bar");
const scaleValue = document.getElementById('scale-value');
scaleSlider.addEventListener('input', ()=> {
    scaleValue.innerHTML = scaleSlider.value + "x";
});


document.getElementById('confirm-rescale-btn').addEventListener('click', async ()=> {
    const formData = new FormData();
    formData.append('scale-value', scaleSlider.value);

    const res = await fetch('/rescale', {
        method: 'POST',
        body: formData
    })

    const blob = await res.blob();
    const imgURL = URL.createObjectURL(blob);
    mosaicURL = imgURL;
    document.getElementById("mosaic-img").src = imgURL; // set up the mosiac picture

    // regenerate the resized original image
    const resOriginal = await fetch('/getOriginal');
    const blobOriginal = await resOriginal.blob();
    originalURL = URL.createObjectURL(blobOriginal);
});








