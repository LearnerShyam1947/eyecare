let image = document.getElementById("image");
let result = document.getElementById("result");
let select = document.getElementById("select");
let submit = document.getElementById("submit");
let spinner = document.getElementById("spinner");
let imageInput = document.getElementById("imageInput");

spinner.style.display = "none";
submit.style.display = 'none';
result.innerHTML = "";

imageInput.onchange = function() {
    result.innerHTML = "";
    renderImage();
    submit.style.display = 'block';
}

function renderImage() {
    let render = new FileReader();
    render.readAsDataURL(imageInput.files[0]);

    console.log(imageInput.files[0]);

    render.onload = () => {
        image.setAttribute('src', render.result);
    };
}

submit.onclick = function() {
    let data = new FormData();
    data.append("image", imageInput.files[0]);

    submit.style.display = 'none';
    spinner.style.display = "block";

    fetch('/api-predict', {
        method: 'POST',
        body: data
    })
    .then((res) => res.json())
    .then((data) => {
        spinner.style.display = "none";
        showResult(data);
    })
    .catch(e => {
        console.log("error");
    })
}

function showResult(data) {
    result.innerHTML = `<h3>Disease : ${data.class}</h3>
                        <h3>Score : ${data.score}</h3>`;
}
