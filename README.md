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


