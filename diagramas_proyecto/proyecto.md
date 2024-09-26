# Descripción General

Este proyecto consiste en un backend desarrollado con **Flask**, **PostgreSQL** y **Stripe** para manejar pagos, mientras que el frontend está desarrollado con **React**, utilizando **Redux** para la gestión de estado, y la configuración de **Firebase**. La aplicación se comunica con una API del backend para mostrar productos, gestionar pagos y realizar otras funcionalidades de comercio electrónico.


# 1. Backend: Flask

El backend está construido con Flask y cuenta con endpoints que permiten obtener los productos y procesar pagos con Stripe.

## Rutas y Funcionalidades

- **`/api/productos` [GET]**: Devuelve la lista de productos disponibles en la base de datos PostgreSQL.
- **`/api/pay` [POST]**: Procesa el pago utilizando Stripe, aceptando la lista de artículos y el correo electrónico del usuario.

# 2. Frontend: React

El frontend utiliza React junto con React Router para gestionar la navegación entre las páginas. También se integra Redux para manejar el estado global y Firebase para la autenticación.

## Estructura de las Páginas

- **`/`**: Página principal que carga los productos.
- **`/about`**: Página de información.
- **`/contact`**: Página de contacto.
- **`/product/:id`**: Página de detalles de producto.
- **`/cart`**: Carrito de compras.
- **`/login`**: Página de inicio de sesión.
- **`/success`**: Página de éxito de pago.



