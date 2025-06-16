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
    document.getElementById('result').innerHTML = 
      document.getElementById('result').innerHTML = `<h3>Result:</h3><img src="${imgURL}" style="max-width:400px;">`;
});


document.getElementById("clean-btn").addEventListener('click', ()=> {
      document.getElementById('result').innerHTML = ``;
})