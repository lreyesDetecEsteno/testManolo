# Audio/Video Transcription Viewer

## Descripción

Esta aplicación web desarrollada con Flask permite subir archivos de audio o video en múltiples formatos junto con un archivo JSON que contiene la transcripción de las palabras, incluyendo información como el hablante, el inicio y fin de cada palabra. La transcripción se muestra sincronizada con el audio/video, permitiendo interactuar con las palabras para controlar la reproducción y resaltar la palabra actual.

## Características

* **Subida de archivos:** Soporta múltiples formatos de audio y video.
* **Sincronización de transcripción:** Las palabras se resaltan en tiempo real según la reproducción.
* **Interacción con la transcripción:** Al hacer clic en una palabra, el reproductor se posiciona en el tiempo correspondiente.
* **Soporte para múltiples hablantes:** Crea bloques separados para cada aparición de un hablante, incluyendo "Speaker Unknown".

## Estructura del Proyecto

```
project/
├── app.py
├── templates/
│   ├── index.html
│   └── view.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── uploads/
│       ├── audio_video_files/
│       └── json_files/
├── requirements.txt
└── README.md
```

## Instalación

### Requisitos

* [Conda](https://docs.conda.io/en/latest/) para la gestión de entornos
* [Python 3.12](https://www.python.org/downloads/)

### Pasos

1. **Clonar el repositorio:**

```bash
git clone https://github.com/lreyesDetecEsteno/testManolo
cd testManolo
```

2. **Crear el entorno con Conda:**

```bash
conda create -n testManolo python==3.12
```

3. **Activar el entorno:**

```bash
conda activate testManolo
```

4. **Instalar las dependencias:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Uso

1. **Ejecutar la aplicación:**

```bash
python app.py
```

2. **Acceder a la aplicación**

Abre tu navegador y dirígete a [http://127.0.0.1:5000/](http://127.0.0.1:5000/) para acceder a la interfaz de subida de archivos.

3. **Subir archivos**

* Selecciona un archivo de audio o video.
* Selecciona el archivo JSON con la transcripción.
* Haz clic en "Subir".

4. **Visualizar la transcripción**

Después de subir los archivos, serás redirigido a una página donde podrás ver la transcripción sincronizada con el audio/video.

## Descripción del JSON

### Claves principales

* **alternatives**
  * Lista de alternativas para la palabra o puntuación detectada.

* **confidence**
  * Nivel de confianza en la detección.

* **content**
  * Contenido de la palabra o puntuación.

* **language**
  * Idioma de la palabra.

* **speaker**
  * Identificador del hablante (e.g., "S1", "S2", "UU").

* **end_time**
  * Tiempo de finalización de la palabra o puntuación en segundos.

* **start_time**
  * Tiempo de inicio de la palabra o puntuación en segundos.

* **type**
  * Tipo de elemento, puede ser:
    * `word`
    * `punctuation`

### Claves opcionales

* **attaches_to**
  * Indica si la puntuación se adjunta a la palabra anterior.

* **is_eos**
  * Indica si es el final de una oración.

## Contribución

¡Contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. **Fork** el repositorio.

2. Crea una nueva rama:

```bash
git checkout -b feature/nueva-funcionalidad
```

3. Realiza tus cambios y commitea:

```bash
git commit -m "Añadir nueva funcionalidad"
```

4. Empuja la rama al repositorio remoto:

```bash
git push origin feature/nueva-funcionalidad
```

5. Abre un **Pull Request**.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para cualquier consulta o sugerencia, puedes contactarme a través de tu correo electrónico.
