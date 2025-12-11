# MoodMirror

MoodMirror es un prototipo de aplicación móvil que analiza emociones a partir de texto e imágenes. La idea es sencilla: ayudar a las personas a entender cómo se sienten día a día sin necesidad de acudir a herramientas complejas o costosas. No pretende reemplazar a un profesional, pero sí ofrecer un espacio accesible para reflexionar y recibir recomendaciones básicas.

Los problemas emocionales y el estrés van en aumento, y conseguir atención psicológica oportuna no siempre es posible: falta de tiempo, costos altos o sistemas de salud saturados. Mucha gente termina ignorando su propio bienestar emocional. MoodMirror nace como una respuesta a esa brecha.

La aplicación combina dos análisis:
- lo que escribes,
- y lo que muestra tu expresión facial.

Con eso obtiene una lectura general de tu estado emocional y te da sugerencias simples para ayudarte a manejarlo mejor, cabe recalcar que esta herramienta no es clínica.

## Componentes del proyecto

MoodMirror está compuesto por tres módulos principales::

1. Un modelo para detección de emociones en texto.
2. Un modelo CNN para detección de emociones en imágenes.
3. Integración móvil


### 1. Modelo de análisis emocional en texto (emotion_detection_text.ipynb)
Modelo basado en XLM-RoBERTa entrenado con datasets públicos. Procesa frases en español y devuelve una emoción entre varias categorías como alegría, ira, tristeza, disgusto, miedo, neutral o sorpresa.

Incluye:
- carga y unión de datasets (se pueden encontrar los datasets usados en los enlaces al inicio del código)
- tokenización
- entrenamiento con HuggingFace
- guardado del modelo (importante para el uso de la aplicación)
- ejemplo de inferencia

### 2. Modelo de análisis emocional en imágenes (emotion_detection_image.ipynb)
Una CNN desarrollada con Keras para clasificar expresiones faciales en diferentes emociones.

Incluye:
- preparación del dataset (el dataset usado se incluye en la carpeta )
- aumentación de datos
- entrenamiento y validación
- matriz de confusión
- guardado del modelo en formato  (importante para el uso de la aplicación)
- ejemplo de predicción con una imagen real


### 3. Aplicación móvil

## Backend FAST API

El backend del proyecto MoodMirror está desarrollado en FastAPI e integra tres componentes principales:
1. Un modelo CNN en TensorFlow para detectar emociones en la imagen.
2. La API de OpenAI para analizar el sentimiento del texto.
3. Una base de datos SQLite donde se almacenan las entradas del diario.

El backend expone varios endpoints que permiten recibir datos desde la aplicación Flutter, procesarlos y devolver los resultados.

--------------------------------------------------------
4.1 Ejecutar el backend
--------------------------------------------------------

Para iniciar el servidor FastAPI, se usa Uvicorn:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

- --host 0.0.0.0 permite que un celular en la misma red pueda acceder al servidor.
- --reload reinicia el servidor automáticamente cuando hay cambios.

El backend quedará disponible en:

http://IP_DEL_SERVIDOR:8000

--------------------------------------------------------
4.2 Archivos principales
--------------------------------------------------------

- main.py → contiene todos los endpoints
- model/*.h5 → modelo CNN para reconocimiento emocional
- db.sqlite3 → base de datos donde se guardan las entradas del diario

--------------------------------------------------------
4.3 Endpoints disponibles
--------------------------------------------------------

(1) POST /add_entry
-------------------

Este endpoint recibe:
- Una foto (UploadFile)
- Un texto escrito por el usuario

El backend ejecuta:
1. Procesamiento de la imagen y predicción de emoción mediante CNN.
2. Análisis del texto usando el modelo de OpenAI.
3. Fusión de ambas emociones para generar un consejo.
4. Guardado de la entrada en la base de datos SQLite.

Retorna un JSON con:
- Fecha de la entrada
- Nota del usuario
- Emoción detectada en la imagen
- Emoción detectada en el texto
- Consejo generado

(2) GET /entries
----------------

Devuelve una lista con todas las entradas almacenadas en SQLite, ordenadas por fecha.
Cada entrada incluye:
- id de registro
- fecha
- texto original
- emoción por imagen
- emoción por texto
- consejo generado

La app Flutter usa este endpoint para mostrar el diario y el progreso semanal.

(3) DELETE /delete_entry/{id}
-----------------------------

Permite eliminar una entrada del diario según su ID.
La aplicación móvil lo usa cuando el usuario quiere borrar una entrada que ya no desea mantener.

--------------------------------------------------------
4.4 Procesos internos del backend
--------------------------------------------------------

- preprocess_image(): Convierte la imagen recibida en un tensor adecuado para la CNN.
- analyze_text_sentiment(): Usa OpenAI para detectar sentimiento del texto.
- generate_advice(): Crea un consejo basado 70% en el texto y 30% en la emoción de la imagen.
- SQLite se usa como almacenamiento local simple para persistencia de entradas.

--------------------------------------------------------
4.5 Requisitos principales del backend
--------------------------------------------------------

pip install fastapi uvicorn tensorflow pillow numpy openai

Además, se debe incluir la clave de OpenAI en:

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

--------------------------------------------------------
4.6 Ejemplo de ejecución exitosa

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     192.168.1.50:54022 - "POST /add_entry HTTP/1.1" 200 OK
INFO:     192.168.1.50:54040 - "GET /entries HTTP/1.1" 200 OK



La aplicación móvil de MoodMirror fue desarrollada en **Flutter**, utilizando un diseño minimalista con tonos pastel y navegación sencilla.  
Para ejecutar el proyecto en cualquier entorno, se deben seguir los siguientes pasos:

---

### Frontend Flutter

La aplicación móvil de MoodMirror fue desarrollada en Flutter, con una interfaz minimalista y temática pastel. Para ejecutar el frontend en cualquier entorno, se deben seguir los siguientes pasos.

------------------------------------------
3.1 Crear un nuevo proyecto Flutter
------------------------------------------

En una terminal:

flutter create moodmirror_app
cd moodmirror_app

Esto genera la estructura base del proyecto.

------------------------------------------
3.2 Instalar las dependencias necesarias
------------------------------------------

Reemplazar el archivo pubspec.yaml creado por Flutter con el archivo pubspec.yaml proporcionado en este repositorio. Este archivo contiene todas las librerías necesarias:

- http (comunicación con backend)
- image_picker (cámara y galería)
- shared_preferences (guardar la IP del servidor)
- flutter_svg (manejo de imágenes SVG)
- Declaración de assets

Después de reemplazarlo, instalar dependencias con:

flutter pub get

------------------------------------------
3.3 Integrar los archivos del frontend
------------------------------------------

Copiar al proyecto Flutter las siguientes carpetas y archivos provenientes del repositorio:

- lib/      (contiene todas las pantallas, widgets y lógica)
- assets/   (imágenes, íconos y recursos gráficos)
- pubspec.yaml (definición de dependencias y assets)

Asegurarse de que en pubspec.yaml esté incluida la declaración:

assets:
  - assets/

------------------------------------------
3.4 Ejecutar la aplicación
------------------------------------------

Para correr la app en un dispositivo físico o emulador:

flutter run

Para generar el APK:

flutter build apk --release

El archivo resultante estará en:

build/app/outputs/flutter-apk/app-release.apk

------------------------------------------
3.5 Conexión con el backend
------------------------------------------

La app requiere la IP del servidor backend. Esto se configura desde la aplicación:

1. Abrir Menú → Configuración
2. Ingresar la IP del backend (solo la IP, sin http:// ni puerto)
3. Guardar cambios y reiniciar la app

Ejemplo:

192.168.1.50

El backend debe ser accesible desde el navegador del celular:

http://IP:8000/entries

------------------------------------------
3.6 Funcionalidades principales
------------------------------------------

- Pantalla de inicio (LoginPage):
  Presenta el logo e ingresa al demo.

- Pantalla principal (HomePage):
  Acceso a Añadir Feeling, Revisar Diario, Análisis de Progreso, Configuración y Nosotros.

- Añadir Feeling:
  Toma una foto, recoge una nota del usuario y envía datos al backend.

- Revisar Diario:
  Muestra todas las entradas almacenadas y permite eliminarlas.

- Análisis de Progreso:
  Resume emociones por día, semana y mes. Detecta patrones repetitivos.

- Configuración:
  Permite guardar la IP del backend utilizando SharedPreferences.

Esta estructura permite instalar, correr y extender el frontend sin dependencias externas adicionales.

