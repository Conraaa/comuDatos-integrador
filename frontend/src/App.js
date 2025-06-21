import React, { useState } from 'react';
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

function App() {
  const [componenteActivo, setComponenteActivo] = useState('analogToDigital');
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [originalImage, setOriginalImage] = useState(null);
  const [selectedBits, setSelectedBits] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [historial, setHistorial] = useState([]);

  const handleCloseOffcanvas = () => setSidebarVisible(false);
  const handleShowOffcanvas = () => setSidebarVisible(true);

  // Función para enviar imagen y bits al backend y recibir la imagen procesada
  const enviarImagenYObtenerProcesadaReduccion = async (imageFile, bits) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      formData.append('bits', bits);

      // Cambia la URL por la de tu backend
      const response = await fetch('http://localhost:5000/api/procesar-imagen', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }

      // Asumimos que el backend devuelve JSON con URL de imagen procesada
      const data = await response.json();

      // data.processedImageUrl = URL de la imagen procesada
      return data.processedImageUrl;

    } catch (error) {
      alert('Error al procesar la imagen: ' + error.message);
      return null;
    }
  };

    const enviarImagenYObtenerProcesadaDigitalizacion = async (imageFile) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      // Cambia la URL por la de tu backend
      const response = await fetch('http://localhost:5000/api/procesar-imagen', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }

      // Asumimos que el backend devuelve JSON con URL de imagen procesada
      const data = await response.json();

      // data.processedImageUrl = URL de la imagen procesada
      return data.processedImageUrl;

    } catch (error) {
      alert('Error al procesar la imagen: ' + error.message);
      return null;
    }
  };


  const handleProcessReduccion = async (imageFile, bits) => {
    // Mostrar la imagen original antes de procesar
    setOriginalImage(URL.createObjectURL(imageFile));
    setSelectedBits(bits);
    setProcessedImage(null); // limpiar resultado previo

    // Enviar al backend y esperar la imagen procesada
    const processedImageUrl = await enviarImagenYObtenerProcesadaReduccion(imageFile, bits);

    if (processedImageUrl) {
      setProcessedImage(processedImageUrl);
      setComponenteActivo('bitDepthResult');
    }
  };




  const handleProcessDigitalizacion = async (imageFile) => {
    setOriginalImage(URL.createObjectURL(imageFile));
    setProcessedImage(null);

    const processedImageUrl = await enviarImagenYObtenerProcesadaDigitalizacion(imageFile);

    if (processedImageUrl) {
      setProcessedImage(processedImageUrl);
      setComponenteActivo('digitizationResult');
    }
  };


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
            <Historial historial={historial} />
        );
      case 'howItWorks':
        return <Funcionamiento />;
      case 'members':
        return <Miembros />;
      default:
        return (
          <Digitalizacion 
            onProcess={handleProcessDigitalizacion}/>
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
