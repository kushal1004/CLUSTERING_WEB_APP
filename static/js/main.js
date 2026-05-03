const dropZone = document.getElementById('dropZone')
const input = document.getElementById('fileInput')
const fileInfo = document.getElementById('fileInfo')
const form = document.getElementById('form')
const loader = document.getElementById('loader')

dropZone.addEventListener('click', () => input.click())

dropZone.addEventListener('dragover', e => {
  e.preventDefault()
  dropZone.classList.add('active')
})

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('active')
})

dropZone.addEventListener('drop', e => {
  e.preventDefault()
  dropZone.classList.remove('active')

  const files = e.dataTransfer.files
  if (files.length > 0) {
    input.files = files
    handleFile(files[0])
  }
})

input.addEventListener('change', e => {
  if (e.target.files.length > 0) {
    handleFile(e.target.files[0])
  }
})

function handleFile (file) {
  if (!file.name.toLowerCase().endsWith('.csv')) {
    fileInfo.innerHTML = '❌ Invalid file (Only CSV allowed)'
    fileInfo.style.color = 'red'
    input.value = '' 
    return
  }

  fileInfo.innerHTML = '✔ ' + file.name
  fileInfo.style.color = '#22c55e'
}

form.addEventListener('submit', () => {
  loader.style.display = 'flex'
})
