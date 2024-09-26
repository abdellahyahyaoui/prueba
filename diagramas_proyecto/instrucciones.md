# Instrucciones para Ejecutar el Proyecto

## 1. Configuración del Backend (Flask)

### Paso 1: Navegar al Directorio del Servidor
1. Abre tu terminal y navega al directorio del servidor donde se encuentra tu aplicación Flask.
    ```bash
    cd server
    ```

### Paso 2: Activar el Entorno Virtual
2. Activa tu entorno virtual donde tienes instaladas las dependencias de Flask.
   - En Windows:
    ```bash
    .\env\Scripts\activate
    ```
   - En macOS/Linux:
    ```bash
    source env/bin/activate
    ```

### Paso 3: Ejecutar la Aplicación Flask
3. Una vez que el entorno virtual esté activado, ejecuta tu aplicación Flask.
    ```bash
    python app.py
    ```
   El servidor de Flask debería comenzar a funcionar y estará disponible en `http://127.0.0.1:5000` 

---

## 2. Configuración del Frontend (React)

### Paso 1: Navegar al Directorio del Cliente
4. Abre otra terminal y navega al directorio del cliente donde se encuentra tu aplicación React.
    ```bash
    cd client
    ```

### Paso 2: Instalar Dependencias (si es necesario)
5. Si es la primera vez que ejecutas el frontend, asegúrate de instalar las dependencias necesarias.
    ```bash
    npm install
    ```

### Paso 3: Ejecutar la Aplicación React
6. Ejecuta tu aplicación React para comenzar el servidor de desarrollo.
    ```bash
    npm run dev
    ```
   Esto abrirá la aplicación en `[ http://localhost:5173/`

---

## 3. Despliegue en Firebase

### Paso 1: Desplegar la Aplicación en Firebase
7. Asegúrate de estar en el directorio del cliente y de tener configurada la autenticación de Firebase. Luego, despliega tu aplicación.
    ```bash
    firebase deploy
    ```
   Esto publicará tu aplicación en Firebase Hosting, y deberías ver la URL donde se encuentra tu aplicación desplegada.
