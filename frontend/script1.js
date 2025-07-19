document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and script running.");
  const form = document.getElementById('uploadForm');
  const uploadBox = document.getElementById('uploadBox');
  const fileInput = document.getElementById('imageInput');
  const fileNameDisplay = document.getElementById('fileNameDisplay');
  const resultSection = document.getElementById('resultSection');
  const extractedTextEl = document.getElementById('extractedText');
  const downloadImageBtn = document.getElementById('downloadImageBtn');
  const downloadTextBtn = document.getElementById('downloadTextBtn');
  const textExtract = document.getElementById('textExtract')


  uploadBox.addEventListener("click", (e) => {
    if (e.target.tagName !== "BUTTON") {
      console.log("Upload Button Activated.")
    }
  });


  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      fileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
      console.log("File Attached.")
    } else {
      fileNameDisplay.textContent = "";
    }
  });


  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Form submit intercepted");

    const file = fileInput.files[0];
    if (!file) {
      alert("Please select an image file.");
      return;
    }

    textExtract.classList.add('hidden');
    const statusEl = document.createElement('p');
    statusEl.id = 'uploadingStatus';
    statusEl.className = 'text-sm text-blue-600 mt-2 text-center';
    statusEl.textContent = 'Processing, please wait...';
    textExtract.parentNode.appendChild(statusEl);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        alert("Failed to upload. Please try again.");
        return;
      }

      const data = await response.json();
      console.log(data);

      extractedTextEl.textContent = Array.isArray(data.extracted_text) ? data.extracted_text.join('\n') : data.extracted_text;

      downloadImageBtn.href = `http://localhost:5000${data.download_image}`;
      downloadImageBtn.setAttribute("download", file.name);

      downloadTextBtn.href = `http://localhost:5000${data.download_text}`;
      downloadTextBtn.setAttribute("download", "extracted_text.txt");

      resultSection.classList.remove('hidden');
      textExtract.classList.add('hidden');
    } catch (error) {
      console.error("Error:", error);
      alert("Server error. Please check backend.");
    } finally {
      textExtract.classList.remove('hidden');
      document.getElementById('uploadingStatus')?.remove();
    }
  });
});
