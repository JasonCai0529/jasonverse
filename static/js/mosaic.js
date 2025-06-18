document.getElementById("uploadForm").addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    const res = await fetch('/generate', {
        method: "POST",
        body: formData
    });

    const blob = await res.blob();
    const imgURL = URL.createObjectURL(blob);
    document.getElementById('output-img').innerHTML = `<h3>Result:</h3><img src="${imgURL}">`;
    document.getElementById("rescale-section").style.display = "block";
});


document.getElementById("clear-btn").addEventListener('click', ()=> {
      location.reload();
});

document.getElementById("clear-img-btn").addEventListener('click', ()=> {
    document.getElementById('output-img').innerHTML = '';
})


const scaleSlider = document.getElementById("scale-bar");
const scaleValue = document.getElementById('scale-value');
scaleSlider.addEventListener('input', ()=> {
    scaleValue.innerHTML = scaleSlider.value + "x";
})


document.getElementById('confirm-rescale-btn').addEventListener('click', async ()=> {
    const formData = new FormData();
    formData.append('scale-value', scaleSlider.value);

    const res = await fetch('/rescale', {
        method: 'POST',
        body: formData
    })
    const blob = await res.blob();
    const imgURL = URL.createObjectURL(blob);
    document.getElementById('output-img').innerHTML = `<h3>Result:</h3><img src="${imgURL}" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
})
