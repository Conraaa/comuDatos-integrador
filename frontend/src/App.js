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
      <header>
        <button className="botonSideBar" onClick={() => setSidebarVisible(!sidebarVisible)}>☰</button>
        <h1>ODigital</h1>
      </header>

      <aside className={sidebarVisible ? 'visible' : ''}>
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

      <footer>
        <p>&copy; 2025 - Comunicación de Datos</p>
      </footer>
    </div>
  );
}

export default App;
