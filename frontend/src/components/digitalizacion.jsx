import React, { useState } from 'react';
import './digitalizacion.css';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [sampleRate, setSampleRate] = useState(1);
  const [quantizationBits, setQuantizationBits] = useState(8);
  const [result, setResult] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) return alert("Seleccione una imagen primero");

    setResult(true);
  };

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit}>
        <h2>Digitalización de Imagen (Simulado)</h2>
        <input type="file" accept="image/*" onChange={e => setFile(e.target.files[0])} />
        <br />
        <label>Frecuencia de muestreo:</label>
        <input type="number" value={sampleRate} onChange={e => setSampleRate(e.target.value)} min="1" />
        <br />
        <label>Bits de cuantización:</label>
        <input type="number" value={quantizationBits} onChange={e => setQuantizationBits(e.target.value)} min="1" max="8" />
        <br />
        <button type="submit">Simular Procesamiento</button>
      </form>

      {result && file && (
        <div className="results">
          <h3>Resultados simulados:</h3>
          <div>
            <p>Imagen Original:</p>
            <img src={URL.createObjectURL(file)} alt="original" />
          </div>
          <div>
            <p>Imagen Procesada (simulada):</p>
            <img src={URL.createObjectURL(file)} alt="procesada" />
          </div>
        </div>
      )}
    </div>
  );
}

export default UploadForm;
