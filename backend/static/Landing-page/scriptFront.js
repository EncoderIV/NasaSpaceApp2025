// --- Default Exoplanet Data (CSV format) ---
const defaultCsvData = `Name,Discovery Year,Mass (Jupiter),Radius (Jupiter),Orbital Period (days),Distance (ly)
Kepler-22b,2011,0.36,2.38,289.9,600
TRAPPIST-1e,2017,0.692,0.91,6.10,40
HD 209458 b,1999,0.69,1.38,3.52,159
Proxima Centauri b,2016,0.003,0.95,11.186,4.2
WASP-12b,2008,1.47,1.83,1.09,870
GJ 1214 b,2009,0.019,2.68,1.58,47
`;

// --- DOM Elements ---
const landingHero = document.getElementById("landing-hero");
const uploadSection = document.getElementById("upload-section");
const exploreBtn = document.getElementById("explore-btn");
const quickBtn = document.getElementById("quick-btn");
const tableArea = document.getElementById("table-area");
const nextBtn = document.getElementById("next-btn");
const fileInfo = document.getElementById("file-info");
const btnArea = document.getElementById("btn-area");
const errorMsg = document.getElementById("error-msg");
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");

let selectedDataset = null; // 'default' or 'custom'
let customCsvText = null;

// --- CSV Parsing ---
function parseCSV(csvString) {
  const lines = csvString.trim().split("\n");
  const result = [];
  for (const line of lines) {
    // Handle quoted values and commas inside quotes
    const values = line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g) || [];
    result.push(values.map((v) => v.replace(/^"|"$/g, "")));
  }
  return result;
}

// --- Table Rendering ---
function renderTable(data) {
  if (!data || data.length < 2) return "";
  let html = "<table><thead><tr>";
  data[0].forEach((header) => {
    html += `<th>${header}</th>`;
  });
  html += "</tr></thead><tbody>";
  for (let i = 1; i < data.length; ++i) {
    html += "<tr>";
    data[i].forEach((cell) => {
      html += `<td>${cell}</td>`;
    });
    html += "</tr>";
  }
  html += "</tbody></table>";
  return html;
}

// --- Landing page buttons ---
exploreBtn.onclick = () => {
  landingHero.style.display = "none";
  uploadSection.style.display = "";
  fileInfo.textContent = "";
  tableArea.innerHTML = "";
  btnArea.innerHTML = "";
  nextBtn.style.display = "none";
};

quickBtn.onclick = () => {
  landingHero.style.display = "none";
  uploadSection.style.display = "none";
  window.location.href = "/loading?dataset=default";
};

// --- Drag & Drop and File Upload ---
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
  dropArea.addEventListener(
    eventName,
    (e) => {
      preventDefaults(e);
      dropArea.classList.add("dragover");
    },
    false
  );
});
["dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(
    eventName,
    (e) => {
      preventDefaults(e);
      dropArea.classList.remove("dragover");
    },
    false
  );
});

dropArea.addEventListener("drop", handleDrop, false);
fileInput.addEventListener("change", handleFiles, false);

function handleDrop(e) {
  errorMsg.textContent = "";
  let dt = e.dataTransfer;
  let files = dt.files;
  handleFiles({ target: { files } });
}

function handleFiles(e) {
  errorMsg.textContent = "";
  const files = e.target.files;
  if (!files || files.length === 0) return;
  const file = files[0];
  if (!file.name.toLowerCase().endsWith(".csv")) {
    errorMsg.textContent = "Please upload a CSV file only!";
    fileInfo.textContent = "";
    return;
  }
  fileInfo.textContent = `Imported: ${file.name}`;
  const reader = new FileReader();
  reader.onload = function (ev) {
    customCsvText = ev.target.result;
    showCustomBtnPreview(customCsvText);
  };
  reader.readAsText(file);
}

// --- Show default data button ---
function showDefaultBtn() {
  btnArea.innerHTML = `<button id="use-default">Use Default Exoplanet Data</button>`;
  document.getElementById("use-default").onclick = () => {
    selectedDataset = "default";
    fileInfo.textContent = "Using default exoplanet data";
    showNextBtn();
    tableArea.innerHTML = renderTable(parseCSV(defaultCsvData));
    btnArea.innerHTML = "";
  };
}

// --- Show custom data button and preview ---
function showCustomBtnPreview(csvText) {
  const data = parseCSV(csvText);
  let previewHtml = '<div class="preview-table-area"><table><thead><tr>';
  data[0].forEach((header) => (previewHtml += `<th>${header}</th>`));
  previewHtml += "</tr></thead><tbody>";
  for (let i = 1; i < Math.min(data.length, 4); ++i) {
    previewHtml += "<tr>";
    data[i].forEach((cell) => (previewHtml += `<td>${cell}</td>`));
    previewHtml += "</tr>";
  }
  previewHtml += "</tbody></table></div>";
  btnArea.innerHTML = `
    <div>Preview of CSV:</div>
    ${previewHtml}
    <button id="use-custom" class="hero-btn preview-btn">Show full CSV table</button>
  `;
  document.getElementById("use-custom").onclick = () => {
    selectedDataset = "custom";
    fileInfo.textContent = "Using custom CSV data";
    showNextBtn();
    tableArea.innerHTML = renderTable(data);
    btnArea.innerHTML = "";
  };
}

// --- Show Next button ---
function showNextBtn() {
  nextBtn.style.display = "inline-block";
}

// --- Next button logic ---
// This version uses the function from your collaborator
nextBtn.onclick = function () {
  // If using the default dataset, redirect to loading with GET
  if (selectedDataset === "default") {
    window.location.href = "/loading?dataset=default";
    return;
  }
  // If custom, upload the file via POST to /loading
  // This assumes fileInput.files[0] is available and valid
  let formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("/loading", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      // Optionally show a message to the user
      // const msg = document.getElementById("error-msg");
      // if (data.success) {
      //   msg.style.color = "green";
      //   msg.innerText = data.message;
      // } else {
      //   msg.style.color = "red";
      //   msg.innerText = data.message;
      // }
      // You might want to redirect to simulation here if training is done:
      // if (data.redirect_url) window.location.href = data.redirect_url;
    })
    .catch(err => {
      console.error(err);
      document.getElementById("error-msg").innerText = "Upload failed";
    });
};

// --- On load: show only landing hero ---
window.addEventListener("DOMContentLoaded", () => {
  landingHero.style.display = "";
  uploadSection.style.display = "none";
  fileInfo.textContent = "";
  tableArea.innerHTML = "";
  btnArea.innerHTML = "";
  nextBtn.style.display = "none";
});