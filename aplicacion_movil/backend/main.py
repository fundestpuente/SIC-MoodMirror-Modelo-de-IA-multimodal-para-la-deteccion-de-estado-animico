import io
import base64
import sqlite3
from datetime import datetime
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import numpy as np
import tensorflow as tf
from openai import OpenAI

# -----------------------------------------------------
# CONFIGURACIONES
# -----------------------------------------------------

app = FastAPI()
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

MODEL_PATH = "model/cnn_moodmirror_64px_50dataset.h5"
IMG_SIZE = (64, 64)

# Cargar modelo CNN
cnn_model = tf.keras.models.load_model(MODEL_PATH)

# Clases originales
CLASS_LABELS = {0: "Angry", 1: "Happy", 2: "Neutral", 3: "Sad", 4: "Surprise"}

# DB SQLite
conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        text_note TEXT,
        image_emotion TEXT,
        text_emotion TEXT,
        advice TEXT
    )
""")
conn.commit()

# -----------------------------------------------------
# UTILIDAD: convertir imagen a tensor
# -----------------------------------------------------
def preprocess_image(file: UploadFile):
    img = Image.open(file.file).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

# -----------------------------------------------------
# UTILIDAD: análisis del texto con OpenAI (sentiment)
# -----------------------------------------------------
def analyze_text_sentiment(text):
    prompt = f"""
    Analiza el sentimiento del siguiente texto y responde SOLO una palabra:
    Angry, Happy, Neutral, Sad o Surprise.

    Texto: "{text}"
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    emotion = resp.choices[0].message.content.strip()
    return emotion

# -----------------------------------------------------
# UTILIDAD: generar el consejo con peso 70% texto / 30% imagen
# -----------------------------------------------------
def generate_advice(text_emotion, image_emotion, note):
    prompt = f"""
    Eres un diario emocional. Debes dar un consejo breve y empático.

    Peso del análisis:
    - 70% basado en el texto
    - 30% basado en la emoción detectada en la imagen

    Emoción por texto: {text_emotion}
    Emoción por imagen: {image_emotion}

    Nota del usuario: "{note}"

    Genera un consejo corto y útil que levante el ánimo.
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content.strip()

# -----------------------------------------------------
# ENDPOINT: registrar entrada diaria
# -----------------------------------------------------

@app.post("/add_entry")
async def add_entry(
    photo: UploadFile,
    text: str = Form(...)
):
    # --- 1. procesar imagen ---
    img_arr = preprocess_image(photo)
    pred = cnn_model.predict(img_arr)[0]   # vector de 5 clases
    emotion_img = CLASS_LABELS[np.argmax(pred)]

    # --- 2. sentimiento por texto ---
    emotion_text = analyze_text_sentiment(text)

    # --- 3. generar consejo ---
    advice = generate_advice(emotion_text, emotion_img, text)

    # --- 4. guardar en SQLite ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO entries (date, text_note, image_emotion, text_emotion, advice)
        VALUES (?, ?, ?, ?, ?)
    """, (now, text, emotion_img, emotion_text, advice))
    conn.commit()

    # --- 5. retornar JSON completo ---
    return {
        "date": now,
        "text_note": text,
        "image": {
            "emotion": emotion_img,
            "scores": pred.tolist()  # probabilidades
        },
        "text": {
            "emotion": emotion_text
        },
        "advice": advice
    }

# -----------------------------------------------------
# ENDPOINT: eliminar entrada por ID
# -----------------------------------------------------
@app.delete("/delete_entry/{entry_id}")
def delete_entry(entry_id: int):
    cur.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    return {"status": "ok", "id": entry_id}


# -----------------------------------------------------
# ENDPOINT: obtener todas las entradas
# -----------------------------------------------------
@app.get("/entries")
def list_entries():
    cur.execute("SELECT * FROM entries ORDER BY date DESC")
    rows = cur.fetchall()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "date": r[1],
            "text_note": r[2],
            "image_emotion": r[3],
            "text_emotion": r[4],
            "advice": r[5]
        })
    return result
