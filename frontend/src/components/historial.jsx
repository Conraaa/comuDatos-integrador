import React from 'react';
import { Container, Row, Col, Card, Spinner, Alert, Button } from 'react-bootstrap';
import './historial.css';

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

function Historial({ historyData, loading, error }) {
  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando historial...</span>
        </Spinner>
        <p className="mt-3">Cargando historial de imágenes...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="py-5">
        <Alert variant="danger">
          Error al cargar el historial: {error}
        </Alert>
      </Container>
    );
  }

  if (!historyData || historyData.length === 0) {
    return (
      <Container className="text-center py-5">
        <p>No hay registros en el historial todavía.</p>
        <p>Procesa algunas imágenes para verlas aquí.</p>
      </Container>
    );
  }

  return (
    <Container className="history-container py-4">
      <h2 className="text-center mb-4">Historial de Procesamiento de Imágenes</h2>
      <Row className="justify-content-center">
        {historyData.map((record, index) => (
          <Col md={10} lg={8} key={index} className="mb-4">
            <Card className="shadow-sm">
              <Card.Header as="h5" className="d-flex justify-content-between align-items-center">
                <span>{record.type === "digitalized" ? "Digitalización" : "Reducción de Bits"}</span>
                <small className="text-muted">{record.original_image.id}</small>
              </Card.Header>
              <Card.Body>
                <Row className="align-items-center">
                  <Col md={4} className="text-center">
                    <h6>Original:</h6>
                    {record.original_image && record.original_image.original_image_url ? (
                      <img src={record.original_image.original_image_url} alt="Original" className="img-fluid history-thumbnail" />
                    ) : (
                      <div className="image-placeholder">No image</div>
                    )}
                    <small className="d-block mt-1">
                      {record.original_image ? record.original_image.filename.split('/').pop() : ''} ({record.original_image ? `${record.original_image.width}x${record.original_image.height}` : ''})
                    </small>
                  </Col>
                  <Col md={1} className="text-center">
                    <div className="display-arrow">{'\u2192'}</div>
                  </Col>
                  <Col md={4} className="text-center">
                    <h6>Procesada:</h6>
                    {record.processed_image_url ? (
                      <img src={record.processed_image_url} alt="Procesada" className="img-fluid history-thumbnail" />
                    ) : (
                      <div className="image-placeholder">No image</div>
                    )}
                    <small className="d-block mt-1">
                      {record.processed_filename ? record.processed_filename.split('/').pop() : ''}
                    </small>
                  </Col>
                  <Col md={3}>
                    {record.type === "digitalized" && (
                      <>
                        <p className="mb-1"><strong>Res. Proc.:</strong> {record.processed_width}x{record.processed_height}</p>
                        <p className="mb-1"><strong>Bits Proc.:</strong> {record.processed_bits_per_channel} bits</p>
                      </>
                    )}
                    {record.type === "bit_reduced" && (
                      <p className="mb-1"><strong>Bits Objetivo:</strong> {record.target_bits_per_channel} bits</p>
                    )}
                    <p className="mb-0 text-muted small">Fecha: {new Date(record.created_at).toLocaleString()}</p>
                    {/* Botón de descarga para la imagen procesada */}
                    {record.processed_image_url && (
                        <Button variant="info" size="sm" className="mt-2" onClick={() => handleDownload(record.processed_image_url, record.processed_filename)}
                        >
                            Descargar
                        </Button>
                    )}
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default Historial;