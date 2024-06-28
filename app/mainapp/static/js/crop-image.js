let cropper;
const input = document.getElementById('self__input-field__photo');


function handleFileInput() {
  const file = input.files[0];
  let button = document.getElementById('self__input-field__crop-button');

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const image = document.getElementById('croppedImage');
      image.src = e.target.result;

      cropper = new Cropper(image, {
        aspectRatio: 1, // Set the aspect ratio as needed
        viewMode: 2,    // Set the view mode (0, 1, 2, 3)
      });
    };

    reader.readAsDataURL(file);
    button.classList.remove('hidden');
  }
}

function uploadCroppedImage() {
  event.preventDefault()

  if (cropper) {
    const croppedCanvas = cropper.getCroppedCanvas();
    const dataURL = croppedCanvas.toDataURL('image/jpeg');
    const list = new DataTransfer();
    const blob = dataURLtoBlob(dataURL);
    const file = new File([blob], 'cropped_image.jpg', {type: 'image/jpeg'});

    list.items.add(file);

    input.files = list.files;
    input.files = list.files;

    document.querySelector("#self__input-field__svg").innerHTML = "";
    document.querySelector("#self__input-field__svg").style.backgroundImage = `url(${dataURL})`;
    document.querySelector("#self__input-field__svg").style.backgroundSize = "100%";
  }
}

function dataURLtoBlob(dataURL) {
  const arr = dataURL.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], {type: mime});
}

input.addEventListener('change', handleFileInput);