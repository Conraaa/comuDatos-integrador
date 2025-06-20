import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './reduccion.css';

function ReduccionResult({ originalImage, processedImage, selectedBits }) {
  return (
    <Container className="reduccion-result-container text-center py-4">
      <Row className="align-items-center mb-4">
        <Col md={5}>
          <h6>Original:</h6>
          <div className="image-preview">
            {originalImage ? (
              <img src={originalImage} alt="Original" className="img-fluid rounded shadow-sm" />
            ) : (
              <div className="image-placeholder">No image</div>
            )}
          </div>
        </Col>

        <Col md={2}>
          <div className="display-6">➡️</div>
        </Col>

        <Col md={5}>
          <h6>{selectedBits} bits depth:</h6>
          <div className="image-preview">
            {processedImage ? (
              <img src={processedImage} alt="Processed" className="img-fluid rounded shadow-sm" />
            ) : (
              <div className="image-placeholder">No image</div>
            )}
          </div>
        </Col>
      </Row>

      <Button variant="info" disabled={!processedImage} onClick={() => {
        // Forzar descarga de imagen procesada
        if (!processedImage) return;
        const link = document.createElement('a');
        link.href = processedImage;
        link.download = 'processed_image.png'; // podés cambiar nombre y extensión
        link.click();
      }}>
        Download
      </Button>
    </Container>
  );
}

export default ReduccionResult;
