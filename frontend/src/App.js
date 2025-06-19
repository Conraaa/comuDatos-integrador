import React, { useState } from 'react';
import './App.css';
import Digitalizacion from './components/digitalizacion';
import Reduccion from './components/reduccion';
import Funcionamiento from './components/funcionamiento';
import Miembros from './components/miembros';

function App() {
  const [componenteActivo, setComponenteActivo] = useState('analogToDigital');
  const [sidebarVisible, setSidebarVisible] = useState(false);

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
        <button className="botonSideBar" onClick={() => setSidebarVisible(!sidebarVisible)}>☰</button>
        <h1>ODigital</h1>
      </header>

      <div className="main-content">
        <aside className={sidebarVisible ? 'visible' : '' }>
            <div className="menuSuperior">
              <button onClick={() => setComponenteActivo('analogToDigital')}>Analog to Digital</button>
              <button onClick={() => setComponenteActivo('bitDepth')}>Lower Bit Depth</button>
            </div>
            <div className="menuInferior">
              <button onClick={() => setComponenteActivo('howItWorks')}>How It Works</button>
              <button onClick={() => setComponenteActivo('members')}>Members</button>
            </div>
        </aside>

        {/* Contenido principal */}
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
