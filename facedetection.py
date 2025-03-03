import cv2
import os
import numpy as np
import sqlite3
import urllib.request
import face_recognition

# URLs for downloading the model files
MODEL_URLS = {
    "prototxt": "https://logeshm05.github.io/deploy.prototxt",
    "caffemodel": "https://logeshm05.github.io/res10_300x300_ssd_iter_140000_fp16.caffemodel"
}

# Define database path
DB_PATH = os.path.join(os.path.expanduser("~"), "face_database.db")

# Global variables
caffe_model = None
stored_encodings = None  # Cache encodings for performance

def get_model_paths():
    """Get internal storage paths for models."""
    base_dir = os.path.expanduser("~")  # Chaquopy internal storage
    model_dir = os.path.join(base_dir, "models")
    os.makedirs(model_dir, exist_ok=True)

    return {
        "prototxt": os.path.join(model_dir, "deploy.prototxt"),
        "caffemodel": os.path.join(model_dir, "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    }

def download_model():
    """Download model files if they don’t exist."""
    paths = get_model_paths()
    for key, path in paths.items():
        if not os.path.exists(path):
            try:
                print(f"Downloading {key} model...")
                urllib.request.urlretrieve(MODEL_URLS[key], path)
            except Exception as e:
                print(f"❌ Error downloading {key}: {e}")
    return paths["prototxt"], paths["caffemodel"]

def load_caffe_model():
    """Load the Caffe model once and reuse it."""
    global caffe_model
    if caffe_model is None:
        try:
            prototxt_path, caffemodel_path = download_model()
            caffe_model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            caffe_model = None
    return caffe_model

def create_database():
    """Create the SQLite database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            encoding BLOB
        )
    """)
    conn.commit()
    conn.close()

def save_face_encoding(encoding):
    """Save face encoding to the SQLite database, ensuring it's 128-dimensional."""
    if encoding.shape != (128,):  # Ensure encoding is correct
        print(f"Invalid encoding shape: {encoding.shape}, skipping save.")
        return None  # Skip invalid encodings
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faces (encoding) VALUES (?)", (encoding.tobytes(),))
    conn.commit()
    conn.close()

def load_stored_encodings():
    """Retrieve stored encodings and filter out any incorrect ones."""
    global stored_encodings
    if stored_encodings is None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT encoding FROM faces")
        
        stored_encodings = []
        for row in cursor.fetchall():
            encoding = np.frombuffer(row[0], dtype=np.float32)
            if encoding.shape == (128,):  # Ensure it's the correct shape
                stored_encodings.append(encoding)
            else:
                print(f"Skipping invalid encoding with shape: {encoding.shape}")

        conn.close()
    return stored_encodings

def extract_face_encoding(image):
    """Extract 128-d feature vector from face using face_recognition."""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)
    return face_encodings[0] if face_encodings else None

def detect_and_recognize_faces(image_path):
    """Detects faces, extracts features, and checks if the user exists in DB."""
    net = load_caffe_model()
    if net is None:
        return "Model loading failed."

    image = cv2.imread(image_path)
    if image is None:
        return "Image not found."

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(300, 300),
                                 mean=(104.0, 177.0, 123.0), swapRB=False, crop=False)
    net.setInput(blob)
    detections = net.forward()

    stored_encodings = load_stored_encodings()  # Load stored face encodings
    results = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")

            face = image[startY:endY, startX:endX]
            if face.size == 0:
                continue

            face_encoding = extract_face_encoding(face)
            if face_encoding is None:
                continue

            is_existing_user = any(np.linalg.norm(stored - face_encoding) < 0.6 for stored in stored_encodings)

            if is_existing_user:
                results.append("Existing User ✅")
            else:
                save_face_encoding(face_encoding)
                results.append("New User ❌")

    return results if results else "Face not detected"

# Run this once to clean up invalid encodings in the database
def clean_invalid_encodings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, encoding FROM faces")

    for row in cursor.fetchall():
        encoding = np.frombuffer(row[1], dtype=np.float32)
        if encoding.shape != (128,):
            print(f"Deleting invalid encoding for ID: {row[0]}, shape: {encoding.shape}")
            cursor.execute("DELETE FROM faces WHERE id=?", (row[0],))

    conn.commit()
    conn.close()
    print("✅ Invalid encodings removed successfully.")
