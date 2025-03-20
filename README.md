# PDF Protector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![PyPDF2](https://img.shields.io/badge/PyPDF2-3.0.1-green.svg)](https://pypdf2.readthedocs.io/)

PDF Protector es una aplicación web que permite a los usuarios restringir la edición de archivos PDF mientras mantiene la capacidad de lectura intacta. Esta herramienta es ideal para compartir documentos que deben ser visualizados pero no modificados.

[English](#english-documentation) | [Español](#documentación-en-español)

![PDF Protector Screenshot](https://via.placeholder.com/800x400?text=PDF+Protector+Screenshot)

## Documentación en Español

### Características

- 🔒 **Protección de PDFs**: Restringe la edición de archivos PDF mientras permite la lectura
- 🌐 **Acceso por navegador**: Interfaz web intuitiva accesible desde cualquier navegador
- 🚀 **Rápido procesamiento**: Protege documentos PDF en segundos
- 🖥️ **Uso local o remoto**: Utilízalo en tu red local o compártelo globalmente mediante ngrok
- 🔄 **Descarga inmediata**: Obtén el archivo protegido al instante
- 🇪🇸 **Interfaz en español**: Aplicación completamente traducida al español

### Instalación

#### Prerrequisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

#### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/virtusdormitiva/pdf-protector.git
   cd pdf-protector
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crear directorios necesarios**
   ```bash
   mkdir uploads protected
   ```

### Uso

#### Uso Local

1. **Iniciar la aplicación**
   ```bash
   python app.py
   ```

2. **Acceder a la aplicación**
   Abre tu navegador y ve a `http://localhost:5000`

3. **Proteger un PDF**
   - Sube un archivo PDF utilizando el botón "Seleccionar archivo"
   - Haz clic en "Subir y Proteger"
   - Una vez procesado, haz clic en "Descargar PDF Protegido"

#### Uso Público con ngrok

Para hacer la aplicación accesible desde internet:

1. **Instalar ngrok**
   - Descarga ngrok desde [https://ngrok.com/download](https://ngrok.com/download)
   - Extrae el archivo y sigue las instrucciones de configuración

2. **Configurar ngrok**
   ```bash
   ngrok config add-authtoken TU_TOKEN_AQUÍ
   ```

3. **Iniciar la aplicación Flask**
   ```bash
   python app.py
   ```

4. **Crear un túnel con ngrok**
   ```bash
   ./ngrok http 5000
   ```

5. **Compartir la URL pública**
   La URL será mostrada en la terminal de ngrok (algo como `https://abcd1234.ngrok-free.app`)

#### Bypass del aviso de ngrok

Para evitar la pantalla de advertencia de ngrok:

1. Abre el archivo `bypass-ngrok.html` incluido en el repositorio
2. Ingresa tu URL de ngrok actual 
3. Haz clic en el botón "Ir a la aplicación"
4. La página configurará automáticamente los ajustes necesarios en tu navegador

### Solución de problemas

- **La aplicación no inicia**: Verifica que Python y todas las dependencias estén instaladas correctamente
- **Error al subir archivos**: Asegúrate de que las carpetas `uploads` y `protected` existan y tengan permisos de escritura
- **El PDF protegido no se descarga**: Verifica que tu navegador no esté bloqueando las descargas
- **Aviso de ngrok persistente**: Limpia la caché del navegador o utiliza la solución bypass-ngrok.html

### Contribuir

Las contribuciones son bienvenidas:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -am 'Agrega nueva funcionalidad'`)
4. Sube los cambios a tu fork (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

### Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## English Documentation

### Features

- 🔒 **PDF Protection**: Restrict editing of PDF files while allowing reading
- 🌐 **Browser Access**: Intuitive web interface accessible from any browser
- 🚀 **Fast Processing**: Protect PDF documents in seconds
- 🖥️ **Local or Remote Use**: Use it on your local network or share it globally using ngrok
- 🔄 **Immediate Download**: Get the protected file instantly
- 🇪🇸 **Spanish Interface**: Application fully translated to Spanish

### Installation

#### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

#### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/virtusdormitiva/pdf-protector.git
   cd pdf-protector
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir uploads protected
   ```

### Usage

#### Local Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the application**
   Open your browser and go to `http://localhost:5000`

3. **Protect a PDF**
   - Upload a PDF file using the "Select file" button
   - Click "Upload and Protect"
   - Once processed, click "Download Protected PDF"

#### Public Usage with ngrok

To make the application accessible from the internet:

1. **Install ngrok**
   - Download ngrok from [https://ngrok.com/download](https://ngrok.com/download)
   - Extract the file and follow the setup instructions

2. **Configure ngrok**
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

3. **Start the Flask application**
   ```bash
   python app.py
   ```

4. **Create a tunnel with ngrok**
   ```bash
   ./ngrok http 5000
   ```

5. **Share the public URL**
   The URL will be displayed in the ngrok terminal (something like `https://abcd1234.ngrok-free.app`)

#### Bypassing the ngrok warning

To avoid the ngrok warning screen:

1. Open the `bypass-ngrok.html` file included in the repository
2. Enter your current ngrok URL
3. Click the "Go to Application" button
4. The page will automatically configure the necessary settings in your browser

### Troubleshooting

- **Application doesn't start**: Verify that Python and all dependencies are correctly installed
- **Error uploading files**: Make sure that the `uploads` and `protected` folders exist and have write permissions
- **Protected PDF doesn't download**: Check if your browser is blocking downloads
- **Persistent ngrok warning**: Clear browser cache or use the bypass-ngrok.html solution

### Contributing

Contributions are welcome:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to your fork (`git push origin feature/new-feature`)
5. Create a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

© 2025 PDF Protector | Raphael Peña

