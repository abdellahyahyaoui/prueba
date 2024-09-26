// src/pages/About.jsx
import React from 'react';

const About = () => {
  return (
    <div className="max-w-screen-md mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Sobre Nosotros</h1>
      <p className="mb-4">
        Somos una empresa dedicada a ofrecer la mejor experiencia de compra en línea. 
        Nuestra misión es brindar productos de alta calidad y un servicio al cliente excepcional.
      </p>
      <h2 className="text-2xl font-semibold mb-2">Nuestra Historia</h2>
      <p className="mb-4">
        Fundada en 2020, comenzamos como un pequeño equipo con una gran pasión por el comercio 
        electrónico. Desde entonces, hemos crecido y hemos expandido nuestra línea de productos.
      </p>
      <h2 className="text-2xl font-semibold mb-2">Nuestra Misión</h2>
      <p>
        Nos comprometemos a ofrecer a nuestros clientes la mejor selección de productos, 
        acompañados de un servicio excepcional y un ambiente de compra seguro y cómodo.
      </p>
    </div>
  );
};

export default About;
