const defaultCsvData = `Name,Discovery Year,Mass (Jupiter),Radius (Jupiter),Orbital Period (days),Distance (ly)
Kepler-22b,2011,0.36,2.38,289.9,600
TRAPPIST-1e,2017,0.692,0.91,6.10,40
HD 209458 b,1999,0.69,1.38,3.52,159
Proxima Centauri b,2016,0.003,0.95,11.186,4.2
WASP-12b,2008,1.47,1.83,1.09,870
GJ 1214 b,2009,0.019,2.68,1.58,47
`;

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

// --- UI Logic ---
const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");
const fileInfo = document.getElementById("file-info");
const tableArea = document.getElementById("table-area");
const errorMsg = document.getElementById("error-msg");
const btnArea = document.getElementById("btn-area");
const nextBtn = document.getElementById("next-btn");
const loadingOverlay = document.getElementById("loading-overlay");

let selectedDataset = null; // 'default' or 'custom'
let customCsvText = null;

// Prevent default drag behaviors
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

// Show default data button
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

// Show custom data button and preview
function showCustomBtnPreview(csvText) {
  const data = parseCSV(csvText);
  let previewHtml = "<table><thead><tr>";
  data[0].forEach((header) => (previewHtml += `<th>${header}</th>`));
  previewHtml += "</tr></thead><tbody>";
  for (let i = 1; i < Math.min(data.length, 4); ++i) {
    previewHtml += "<tr>";
    data[i].forEach((cell) => (previewHtml += `<td>${cell}</td>`));
    previewHtml += "</tr>";
  }
  previewHtml += "</tbody></table>";
  btnArea.innerHTML = `
    <div>Preview of CSV:</div>
    ${previewHtml}
    <button id="use-custom">Use Custom CSV Data</button>
  `;
  document.getElementById("use-custom").onclick = () => {
    selectedDataset = "custom";
    fileInfo.textContent = "Using custom CSV data";
    showNextBtn();
    tableArea.innerHTML = renderTable(data);
    btnArea.innerHTML = "";
  };
}

// Show Next button
function showNextBtn() {
  nextBtn.style.display = "inline-block";
}

// Next button logic
nextBtn.onclick = function () {
  // Show loading overlay
  loadingOverlay.style.display = "flex";
  // Simulate ML model call (replace with actual call if needed)
  setTimeout(() => {
    loadingOverlay.style.display = "none";
    // After prediction, show some results (replace with actual results)
    tableArea.innerHTML =
      "<h2>Prediction Done!</h2><p>See exoplanet prediction results below.</p>";
    // Optionally: render prediction results table here
  }, 3000); // Simulate 3 seconds ML processing
};

// On load: show only button to use default
window.addEventListener("DOMContentLoaded", () => {
  fileInfo.textContent = "";
  tableArea.innerHTML = "";
  showDefaultBtn();
  nextBtn.style.display = "none";
});
