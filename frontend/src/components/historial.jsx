import React from 'react';
import './historial.css';

function Historial({ historial }) {
  return (
    <div className="historial-container">
      <h2>Historial de imágenes procesadas</h2>
      <div className="card-grid">
        {historial.map((item, index) => (
          <div className="historial-card" key={index}>
            <p><strong>{item.tipo}</strong></p>
            {/*<img src={item.original} alt="Original" />*/}
            <img src={item.procesada} alt="Procesada" />
            {item.bits && <p>Bits: {item.bits}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Historial;
