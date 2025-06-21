import React, { useState } from 'react';
import { Container, Button, Form } from 'react-bootstrap';
import './digitalizacion.css';
import { message } from 'antd';


function Digitalizacion({ onProcess }) {
  const [fileName, setFileName] = useState('');
  const [file, setFile] = useState(null);

  const FIXED_SAMPLE_RATE = 10;
  const FIXED_QUANTIZATION_BITS = 5;

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setFileName(selected.name);
    } else {
      setFile(null);
      setFileName('');
    }
  };

  const handleProcessDigitalizacion = () => {
    if (!file) {
      message.error("Select file first.");
      return;
    }
    onProcess(file, FIXED_SAMPLE_RATE, FIXED_QUANTIZATION_BITS);
  };

  return (
    <Container className="digitalizacion-card-container">
      <div className="upload-card text-center">
        <h2 className="mb-4">Analog to Digital</h2>
        <div className="upload-icon">☁️</div>

        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label className="btn btn-primary mb-2">Choose file to upload</Form.Label>
          <Form.Control
            type="file"
            className="d-none"
            onChange={handleFileChange}
          />
          <div className="file-name text-muted small">
            {fileName ? <span>Selected file: <strong>{fileName}</strong></span> : 'No file selected'}
          </div>
        </Form.Group>

        <Button variant="success" onClick={handleProcessDigitalizacion}>Process</Button>
      </div>
    </Container>
  );
}

export default Digitalizacion;