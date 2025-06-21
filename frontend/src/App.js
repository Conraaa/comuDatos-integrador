import React, { useState, useEffect } from 'react';
import './App.css';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button';
import ReduccionResult from './components/reduccion-result';
import Digitalizacion from './components/digitalizacion';
import DigitalizacionResult from './components/digitalizacion-result';
import Reduccion from './components/reduccion';
import Funcionamiento from './components/funcionamiento';
import Miembros from './components/miembros';
import Historial from './components/historial';
import miImagen from './circle logo.png';
import logoMenu from './png logo.png';
import { message } from 'antd';

function App() {
  const [componenteActivo, setComponenteActivo] = useState('analogToDigital');
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [originalImage, setOriginalImage] = useState(null);
  const [selectedBits, setSelectedBits] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [historyData, setHistoryData] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState(null);

  const handleCloseOffcanvas = () => setSidebarVisible(false);
  const handleShowOffcanvas = () => setSidebarVisible(true);

  // url backend
  const BACKEND_BASE_URL = 'http://127.0.0.1:8000';


  // digitalizacion
  const enviarImagenYObtenerProcesadaDigitalizacion = async (imageFile, sampleRate, quantizationBits) => {
    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      formData.append('sample_rate', sampleRate);
      formData.append('quantization_bits', quantizationBits);

      const response = await fetch(`${BACKEND_BASE_URL}/upload-and-process/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error en la respuesta del servidor para digitalización');
      }

      const data = await response.json();

      return {
        original_image_url: `${BACKEND_BASE_URL}${data.original_image_url}`,
        processed_image_url: `${BACKEND_BASE_URL}${data.processed_image_url}`
      };

    } catch (error) {
      message.error('Error al procesar la imagen: ' + error.message);
      return null;
    }
  };


  // reduccion
  const enviarImagenYObtenerProcesadaReduccion = async (imageFile, targetBits) => {
    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      formData.append('target_bits', targetBits);

      const response = await fetch(`${BACKEND_BASE_URL}/reduce-bits/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error en la respuesta del servidor para reducción de bits');
      }

      const data = await response.json();

      return {
        original_image_url: `${BACKEND_BASE_URL}${data.original_image_url}`,
        processed_image_url: `${BACKEND_BASE_URL}${data.processed_image_url}`
      };

    } catch (error) {
      alert('Error al procesar la imagen (Reducción de Bits): ' + error.message);
      return null;
    }
  };


  // handle digitalizacion
  const handleProcessDigitalizacion = async (imageFile, sampleRate, quantizationBits) => {
    setOriginalImage(URL.createObjectURL(imageFile));
    setProcessedImage(null);

    const processedUrls = await enviarImagenYObtenerProcesadaDigitalizacion(imageFile, sampleRate, quantizationBits);

    if (processedUrls) {
      setOriginalImage(processedUrls.original_image_url);
      setProcessedImage(processedUrls.processed_image_url);
      setComponenteActivo('digitizationResult');
      fetchHistory();
    }
  };


  // handle reduccion
  const handleProcessReduccion = async (imageFile, targetBits) => {
    setOriginalImage(URL.createObjectURL(imageFile));
    setSelectedBits(targetBits);
    setProcessedImage(null);

    const processedUrls = await enviarImagenYObtenerProcesadaReduccion(imageFile, targetBits);

    if (processedUrls) {
      setOriginalImage(processedUrls.original_image_url);
      setProcessedImage(processedUrls.processed_image_url);
      setComponenteActivo('bitDepthResult');
      fetchHistory();
    }
  };


  // historial
  const fetchHistory = async () => {
    setHistoryLoading(true);
    setHistoryError(null);
    try {
      const response = await fetch(`${BACKEND_BASE_URL}/history/`);
      if (!response.ok) {
        throw new Error('Error al cargar el historial.');
      }
      const data = await response.json();
      setHistoryData(data);
    } catch (error) {
      setHistoryError(error.message);
      console.error('Error cargando historial:', error);
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    if (componenteActivo === 'history') {
      fetchHistory();
    }
  }, [componenteActivo]);




  const renderComponente = () => {
    switch (componenteActivo) {
      case 'bitDepth':
        return (
          <Reduccion
            onProcess={handleProcessReduccion}
          />
        );
      case 'bitDepthResult':
        return (
          <ReduccionResult
            originalImage={originalImage}
            processedImage={processedImage}
            selectedBits={selectedBits}
          />
        );
      case 'digitizationResult':
        return (
          <DigitalizacionResult
            originalImage={originalImage}
            processedImage={processedImage}
          />
        );
      case 'history':
        return (
          <Historial
            historyData={historyData}
            loading={historyLoading}
            error={historyError}
          />
        );
      case 'howItWorks':
        return <Funcionamiento />;
      case 'members':
        return <Miembros />;
      default:
        return (
          <Digitalizacion 
            onProcess={handleProcessDigitalizacion}
          />
        );
    }
  };

 


  return (
    <div className="app-container">
      <header className='header'>
        <button className="botonSideBar" onClick={handleShowOffcanvas}>☰</button>
        <h1>ODigital</h1>
      </header>

      <div className="main-content">
        <Offcanvas show={sidebarVisible} onHide={handleCloseOffcanvas} placement="start">
          <Offcanvas.Header closeButton>
            <Offcanvas.Title>
              <img className="logo-Menu" src={logoMenu} alt="Logo" />
              Menú ODigital</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>
            <div className="menuSuperior">
              {/*Boton de Analog*/}
              <Button
                variant="light"
                onClick={() => { setComponenteActivo('analogToDigital'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'analogToDigital' ? 'active-link' : ''}
              >
                Analog to Digital
              </Button>

              {/*Boton de Bits*/}
              <Button
                variant="light"
                onClick={() => { setComponenteActivo('bitDepth'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'bitDepth' ? 'active-link' : ''}
              >
                Lower Bit Depth
              </Button>

              {/*Boton de Historial*/}
              <Button
                variant="light"
                onClick={() => { setComponenteActivo('history'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'history' ? 'active-link' : ''}
              >
                History
              </Button>
            </div>
            <hr />
            <div className="menuInferior">
              {/*Boton de How it Works*/}
              <Button
                variant="light"
                onClick={() => { setComponenteActivo('howItWorks'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'howItWorks' ? 'active-link' : ''}
              >
                How It Works
              </Button>

              {/*Boton de Members*/}
              <Button
                variant="light"
                onClick={() => { setComponenteActivo('members'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'members' ? 'active-link' : ''}
              >
                Members
              </Button>
            </div>
          </Offcanvas.Body>
        </Offcanvas>

        <main>
          {renderComponente()}
        </main>
      </div>

      <footer className='footer'>
        <div className="footer-top">
          <div className="footer-left">
            <img className="logo-Footer" src={miImagen} alt="Logo" />

          </div>
          <div className="footer-column-right">
            <div className='footer-column-section'>
              <p className="footer-title"><b>ODigital</b></p>
              <ul>
                <li><a href="#" onClick={(e) => { e.preventDefault(); setComponenteActivo('howItWorks'); }}>How It Works</a></li>
                <li><a href="#" onClick={(e) => { e.preventDefault(); setComponenteActivo('members'); }}>Members</a></li>
              </ul>
            </div>
            <div className='footer-column-section'>
              <p className="footer-title"><b>New Photograph</b></p>
              <ul>
                <li><a href="#" onClick={(e) => { e.preventDefault(); setComponenteActivo('analogToDigital'); }}>Analog to Digital</a></li>
                <li><a href="#" onClick={(e) => { e.preventDefault(); setComponenteActivo('bitDepth'); }}>Lower Bit Depth</a></li>
              </ul>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          &copy; 2025 ODigital. All Rights Reserved
        </div>
      </footer>
    </div>
  );
}

export default App;