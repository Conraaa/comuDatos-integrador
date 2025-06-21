import React from 'react';
import './funcionamiento.css';

function funcionamiento() {
  const cards = [
    { numero: 1, texto: 'Selecciona una opción en el menú.' },
    { numero: 2, texto: 'Si elegiste la reducción de bits, selecciona la profundidad de bits que quiere para tu imagen final.' },
    { numero: 3, texto:  'Sube tu imagen.'},
    { numero: 4, texto: 'Descárgala.' },
    { numero: 5, texto: 'Selecciona "History" en el menú para visualizar tu historial.' },
  ];

  return (
    <div className="card-grid-container">
      <h2>¿Cómo funciona?</h2>
      <div className="card-grid">
        {cards.map((card, index) => (
          <div className="card-f" key={index}>
            <div className="icono-estilizado">{card.numero}</div>
            <p>{card.texto}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default funcionamiento;