import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './reduccion-result.css';

function ReduccionResult({ originalImage, processedImage, selectedBits }) {
  const handleDownload = async (imageUrl, filename) => {
    try {
      const response = await fetch(imageUrl);
      if (!response.ok) {
        throw new Error('Error al descargar la imagen: ' + response.statusText);
      }
      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error('Error al iniciar la descarga:', err);
      alert('No se pudo descargar la imagen: ' + err.message);
    }
  };

  return (
    <Container className="reduccion-result-container text-center py-4">
      <Row className="align-items-center mb-4">
        <Col md={5}>
          <h6 className="desc">Original:</h6>
          <div className="image-preview">
            {originalImage ? (
              <img src={originalImage} alt="Original" className="img-fluid rounded shadow-sm" />
            ) : (
              <div className="image-placeholder">No image</div>
            )}
          </div>
        </Col>

        <Col md={2}>
          <div className="display-6">{'\u2192'}</div>
        </Col>

        <Col md={5}>
          <h6 className="desc">{selectedBits} bits depth:</h6>
          <div className="image-preview">
            {processedImage ? (
              <img src={processedImage} alt="Processed" className="img-fluid rounded shadow-sm" />
            ) : (
              <div className="image-placeholder">No image</div>
            )}
          </div>
        </Col>
      </Row>

      <Button className="btn-custom-purple" disabled={!processedImage} onClick={() => handleDownload(processedImage, `imagen_reducida_${selectedBits}bits.png`)}
      >
        Download
      </Button>
    </Container>
  );
}

export default ReduccionResult;
