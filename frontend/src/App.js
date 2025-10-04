import React, { useCallback, useState } from "react";

export default function FileUploader() {
  const [fileName, setFileName] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const readFile = useCallback((file) => {
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (e) => {
      // create a small text preview (first ~10 lines)
      const text = String(e.target.result || "");
      const lines = text
        .replace(/\r\n/g, "\n")
        .replace(/\r/g, "\n")
        .split("\n")
        .slice(0, 10);
      setPreview(lines);
    };
    reader.readAsText(file);
  }, []);

  const onDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragOver(false);
      const f = e.dataTransfer?.files?.[0];
      if (f) readFile(f);
    },
    [readFile]
  );

  const onFileInput = useCallback(
    (e) => {
      const f = e.target.files?.[0];
      if (f) readFile(f);
    },
    [readFile]
  );

  const onSkip = useCallback(() => {
    const DEFAULT_CSV = `name,mass,orbit_period,discovery_method\nKepler-22b,2.4,289.9,Transit\nKepler-452b,5.0,384.8,Transit`; // this would be where we set up the access to some of the nasa conrimed exoplanet
    const lines = DEFAULT_CSV.split("\n").slice(0, 10);
    setFileName("Default dataset");
    setPreview(lines);
  }, []);

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#000",
        color: "#fff",
        padding: 24,
        boxSizing: "border-box",
        fontFamily:
          "Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial",
      }}
    >
      <div style={{ width: 920, maxWidth: "100%", textAlign: "center" }}>
        <h1 style={{ margin: 0, marginBottom: 12, fontSize: 28 }}>
          Exoplanet Explorer — Upload CSV
        </h1>
        <p style={{ marginTop: 0, marginBottom: 20, opacity: 0.8 }}>
          Drag & drop a CSV file, click to choose one, or use the default
          dataset.
        </p>

        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={onDrop}
          style={{
            border: `2px dashed ${dragOver ? "#66ff66" : "#444"}`,
            borderRadius: 12,
            padding: 28,
            cursor: "pointer",
            background: dragOver ? "rgba(102,255,102,0.04)" : "transparent",
            transition: "all 120ms ease",
          }}
          onClick={() =>
            document.getElementById("file-input-react-uploader")?.click()
          }
        >
          <div style={{ pointerEvents: "none" }}>
            <strong style={{ fontSize: 16 }}>Drop CSV here</strong>
            <div style={{ height: 8 }} />
            <span style={{ opacity: 0.8 }}>or click to browse</span>
          </div>

          <input
            id="file-input-react-uploader"
            type="file"
            accept=".csv,text/csv"
            onChange={onFileInput}
            style={{ display: "none" }}
          />
        </div>

        <div
          style={{
            marginTop: 16,
            display: "flex",
            gap: 12,
            justifyContent: "center",
          }}
        >
          <button
            onClick={onSkip}
            style={{
              background: "#111",
              border: "1px solid #333",
              color: "#fff",
              padding: "10px 16px",
              borderRadius: 8,
              cursor: "pointer",
            }}
          >
            Use Default Dataset
          </button>

          <button
            onClick={() =>
              alert("Placeholder: Run prediction (connect to backend)")
            }
            style={{
              background: "#0b84ff",
              border: "none",
              color: "#fff",
              padding: "10px 16px",
              borderRadius: 8,
              cursor: "pointer",
            }}
            disabled={!fileName}
            title={
              fileName
                ? "Run prediction on uploaded dataset"
                : "Upload or skip to enable"
            }
          >
            Run Prediction
          </button>
        </div>

        <div
          style={{
            marginTop: 22,
            textAlign: "left",
            background: "#050505",
            border: "1px solid #111",
            padding: 16,
            borderRadius: 10,
          }}
        >
          <div style={{ fontSize: 13, color: "#9aa0a6" }}>Selected file:</div>
          <div style={{ fontSize: 15, marginTop: 6 }}>
            {fileName ?? "No file selected"}
          </div>

          <div style={{ height: 12 }} />

          <div style={{ fontSize: 13, color: "#9aa0a6" }}>
            Preview (first 10 lines):
          </div>
          <pre
            style={{
              whiteSpace: "pre-wrap",
              marginTop: 8,
              fontSize: 13,
              lineHeight: 1.4,
            }}
          >
            {preview ? preview.join("\n") : "—"}
          </pre>
        </div>
      </div>
    </div>
  );
}
