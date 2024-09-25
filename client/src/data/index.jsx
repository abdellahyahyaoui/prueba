import axios from "axios";

export const getProducts = async () => {
  const products = await axios.get(
    "https://prueba-1-1qb5.onrender.com/api/productos"
  );
  return products;
};
