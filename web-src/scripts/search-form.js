const tabState = {'active': 'Image'}
const tabElements = document.querySelectorAll('.tab-element')
const tabView = document.querySelector('.tab-view')
const imageField = document.getElementById('image-field')
const textField = document.getElementById('text-field')
const keyField = document.getElementById('key-field')
const imageHolderPath = 'web-src/resources/loadingholder.gif'
const imageSample = document.querySelector('.img-element')
const imgContainer = document.getElementById('img-container')
const searchButton = document.getElementById('search-button')
const previewImage = document.getElementById('preview-image')
imgContainer.innerHTML=""
tabElements.forEach(tabElement => {
    tabElement.addEventListener('click', () => {
        tabState.active = tabElement.textContent
        console.log(tabState.active)
        tabElements.forEach(tabElement => {
        tabElement.classList.remove('tab-element-active')
        })
        tabElement.classList.add('tab-element-active')
        if (tabState.active === 'Image') {
            imageField.style.display = 'block'
            textField.style.display = 'none'
            keyField.style.display = 'none'
        } else if (tabState.active === 'Text') {
            imageField.style.display = 'none'
            textField.style.display = 'block'
            keyField.style.display = 'none'
        } else {
            imageField.style.display = 'block'
            textField.style.display = 'block'
            keyField.style.display = 'block'
        }
    })
    })
textField.style.display = 'none'
keyField.style.display = 'none'

const imageInput = document.getElementById('in-image')
const textInput = document.getElementById('in-text')
const keyInput = document.getElementById('api-key')

async function search(){
    var number_of_images = sliderk.value;
    const formData = new FormData()
    formData.append('k', number_of_images)
    if (tabState.active === 'Image') {
        const image = imageInput.files[0]
        if (image) {
            formData.append('image', image)
            try {
                searchButton.disabled = true
                preRenderImage(number_of_images)
                previewImage.src = URL.createObjectURL(image)
                previewImage.style.display = 'block'    
                const response = await fetch('http://127.0.0.1:8000/search/image', {
                    method: 'POST',
                    body: formData
                })
                const data = await response.json()
                renderImage(data)
                searchButton.disabled = false
            } catch (error) {
                console.error(error)
                searchButton.disabled = false
                clearImage()
                alert("We are sorry, the server is not available at the moment. Please try again later.")

            }
        }
    } else if (tabState.active === 'Text') {
        const text = textInput.value
        if (text) {
            formData.append('query', text)
            console.log(formData)
            try {
                searchButton.disabled = true
                previewImage.style.display = 'none'
                preRenderImage(number_of_images)
                const response = await fetch('http://127.0.0.1:8000/search/text', {
                    method: 'POST',
                    body: formData
                })
                const data = await response.json()
                renderImage(data)
                searchButton.disabled = false
            } catch (error) {
                console.error(error)
                searchButton.disabled = false
                clearImage()
                alert("We are sorry, the server is not available at the moment. Please try again later.")
            }
        }
    } else {
        const image = imageInput.files[0]
        const text = textInput.value
        const key = keyInput.value
        if (image && text) {
            formData.append('image', image)
            formData.append('query', text)
            formData.append('api_key', key)
            try {
                searchButton.disabled = true
                preRenderImage(number_of_images)
                previewImage.src = URL.createObjectURL(image)
                previewImage.style.display = 'block'
                const response = await fetch('http://127.0.0.1:8000/search/composed', {
                    method: 'POST',
                    body: formData
                })
                const data = await response.json()
                renderImage(data)
                searchButton.disabled = false
            } catch (error) {
                console.error(error)
                searchButton.disabled = false
                clearImage()
                alert("We are sorry, the server is not available at the moment. Please try again later.")

            }
        }
    }
}
function preRenderImage(number_of_images) {
    imgContainer.innerHTML=""
    for (var i = 0; i < number_of_images; i++) {
        var imgageElement = imageSample.cloneNode(true);
        imgageElement.querySelector('img').src = imageHolderPath;
        imgContainer.appendChild(imgageElement);
    }
}
function clearImage() {
    imgContainer.innerHTML=""
}
function renderImage(list_image_path) {
    imageElements = imgContainer.querySelectorAll('.img-element>img')
    for (var i = 0; i < list_image_path.length; i++) {
        imageElements[i].src = list_image_path[i];
    }
}