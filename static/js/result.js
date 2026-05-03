function showTab (evt, id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'))
  document
    .querySelectorAll('.tab-content')
    .forEach(c => c.classList.remove('active'))
  evt.currentTarget.classList.add('active')
  document.getElementById(id).classList.add('active')
}

function openModal (img) {
  document.getElementById('imgModal').style.display = 'flex'
  document.getElementById('modalImg').src = img.src
}

function closeModal () {
  document.getElementById('imgModal').style.display = 'none'
}

function downloadImage (url) {
  const a = document.createElement('a')
  a.href = url
  a.download = 'graph.png'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
