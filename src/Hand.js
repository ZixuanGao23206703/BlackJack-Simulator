import React from 'react';

const Hand = ({ cards }) => (
  <>
    {cards.map((card, index) => (
      <img key={index} src={card.image} alt={card.code} className="card-image" />
    ))}
  </>
);

export default Hand;