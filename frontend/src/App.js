import React, { useState } from 'react';
import './App.css';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button'; 

import Digitalizacion from './components/digitalizacion';
import Reduccion from './components/reduccion';
import Funcionamiento from './components/funcionamiento';
import Miembros from './components/miembros';

function App() {
  const [componenteActivo, setComponenteActivo] = useState('analogToDigital');
  const [sidebarVisible, setSidebarVisible] = useState(false); 

  const handleCloseOffcanvas = () => setSidebarVisible(false);
  const handleShowOffcanvas = () => setSidebarVisible(true);

  const renderComponente = () => {
    switch (componenteActivo) {
      case 'bitDepth': return <Reduccion />;
      case 'howItWorks': return <Funcionamiento />;
      case 'members': return <Miembros />;
      default: return <Digitalizacion />;
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
            <Offcanvas.Title>Menú ODigital</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>
          
            <div className="menuSuperior">
              <Button
                variant="light" 
                onClick={() => { setComponenteActivo('analogToDigital'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'analogToDigital' ? 'active-link' : ''}
              >
                Analog to Digital
              </Button>
              <Button
                variant="light"
                onClick={() => { setComponenteActivo('bitDepth'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'bitDepth' ? 'active-link' : ''}
              >
                Lower Bit Depth
              </Button>
            </div>
            <hr /> 
            <div className="menuInferior">
              <Button
                variant="light"
                onClick={() => { setComponenteActivo('howItWorks'); handleCloseOffcanvas(); }}
                className={componenteActivo === 'howItWorks' ? 'active-link' : ''}
              >
                How It Works
              </Button>
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
            <p><strong>logo</strong></p>
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
          <p>&copy; 2025 ODigital. All Rights Reserved</p>
        </div>
      </footer>
    </div>
  );
}

export default App;