document.addEventListener('DOMContentLoaded', () => {
  const dropZone = document.getElementById('dropZone')

  const fileInput = document.getElementById('fileInput')

  const uploadForm = document.getElementById('uploadForm')

  const loader = document.getElementById('loader')

  const originalContent = `

        <div class="upload-content">

            <div class="upload-icon">
                ⬆
            </div>

            <h3>
                Drag & Drop Dataset
            </h3>

            <p>
                or click to browse files
            </p>

            <div class="supported">
                Supports CSV files
            </div>

        </div>
    `

  dropZone.addEventListener('click', () => {
    fileInput.click()
  })

  dropZone.addEventListener('dragover', e => {
    e.preventDefault()

    dropZone.classList.add('dragover')
  })

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover')
  })

  dropZone.addEventListener('drop', e => {
    e.preventDefault()

    dropZone.classList.remove('dragover')

    const files = e.dataTransfer.files

    if (files.length > 0) {
      fileInput.files = files

      updateFile(files[0])
    }
  })

  fileInput.addEventListener('change', e => {
    if (e.target.files.length > 0) {
      updateFile(e.target.files[0])
    }
  })

  function updateFile (file) {
    if (!file.name.toLowerCase().endsWith('.csv')) {
      dropZone.querySelector('.upload-content').innerHTML = `

                <div class="upload-icon">
                    ❌
                </div>

                <h3>
                    Invalid File
                </h3>

                <p>
                    Please upload CSV file only
                </p>
            `

      return
    }

    dropZone.querySelector('.upload-content').innerHTML = `

            <div class="upload-success">

                <div class="success-icon">
                    ✔
                </div>

                <h3>
                    ${file.name}
                </h3>

                <p>
                    ${(file.size / 1024).toFixed(2)} KB Uploaded Successfully
                </p>

                <div class="change-file">
                    Click to change file
                </div>

            </div>
        `
  }

  uploadForm.addEventListener('submit', () => {
    loader.style.display = 'flex'
  })
})
