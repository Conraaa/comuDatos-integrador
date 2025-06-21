import React, { useState } from 'react';
import { Container, Button, Form } from 'react-bootstrap';
import './reduccion.css';
import { message } from 'antd';

function Reduccion({ onProcess }) {
  const [selectedBitDepth, setSelectedBitDepth] = useState(null);
  const [fileName, setFileName] = useState('');
  const [file, setFile] = useState(null);

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

  const handleProcessReduccion = () => {
    if (!file || !selectedBitDepth) {
      message.error("Select file and bit depth first.");
      return;
    }
    onProcess(file, parseInt(selectedBitDepth, 10));
  };

  return (
    <Container className="reduccion-card-container">
      <div className="upload-card text-center">
        <h2 className="mb-4">Lower Bit Depth</h2>
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

        <div className="bit-buttons mt-3 mb-4 d-flex justify-content-center flex-wrap gap-2">
          {[1, 2, 3, 4, 5, 6, 7, 8, 24].map((bit) => (
            <Button
              key={bit}
              className={`bit-button ${selectedBitDepth === bit ? 'active' : ''}`}
              onClick={() => setSelectedBitDepth(bit)}
            >
              {bit} Bit{bit > 1 ? 's' : ''}
            </Button>
          ))}
        </div>

        <Button variant="success" onClick={handleProcessReduccion}>Process</Button>
      </div>
    </Container>
  );
}

export default Reduccion;
