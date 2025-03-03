import cv2
import os
import urllib.request
import sqlite3
import numpy as np

# URLs for downloading the model files
MODEL_URLS = {
    "prototxt": "https://logeshm05.github.io/deploy.prototxt",
    "caffemodel": "https://logeshm05.github.io/res10_300x300_ssd_iter_140000_fp16.caffemodel"
}

DB_PATH = os.path.join(os.path.expanduser("~"), "face_data.db")

# Load the Caffe model globally
caffe_model = None

def get_model_paths():
    """Get internal storage paths for models in Android."""
    base_dir = os.path.expanduser("~")  # Chaquopy internal storage
    model_dir = os.path.join(base_dir, "models")
    os.makedirs(model_dir, exist_ok=True)  # Ensure the directory exists

    return {
        "prototxt": os.path.join(model_dir, "deploy.prototxt"),
        "caffemodel": os.path.join(model_dir, "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    }

def download_model():
    """Download model files if they don’t exist in the internal storage."""
    paths = get_model_paths()
    for key, path in paths.items():
        if not os.path.exists(path):
            print(f"Downloading {key} model...")
            urllib.request.urlretrieve(MODEL_URLS[key], path)

    return paths["prototxt"], paths["caffemodel"]

def load_caffe_model():
    """Load the Caffe model only once and reuse it."""
    global caffe_model
    if caffe_model is None:
        try:
            prototxt_path, caffemodel_path = download_model()  # Downloads if not present
            caffe_model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            caffe_model = None

    return caffe_model

def init_db():
    """Initialize SQLite database to store face encodings."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            encoding BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def extract_face_encoding(image):
    """Extracts facial features as a NumPy array (simulating face embeddings)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.array(gray.flatten(), dtype=np.float32)[:128]  # Simulating 128-d embedding

def recognize_face(image_encoding):
    """Compare the detected face encoding with stored encodings."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT encoding FROM faces")
    stored_encodings = cursor.fetchall()
    conn.close()

    if not stored_encodings:
        return False  # No faces stored yet

    stored_encodings = [np.frombuffer(enc[0], dtype=np.float32) for enc in stored_encodings]

    for stored_encoding in stored_encodings:
        distance = np.linalg.norm(stored_encoding - image_encoding)
        if distance < 1000:  # Set a threshold (tune as needed)
            return True

    return False

def detect_and_recognize_faces(image_path):
    """Detects faces, extracts features, and checks if the user exists in the DB."""
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

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            # Get bounding box
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")

            # Crop and extract facial features
            face = image[startY:endY, startX:endX]
            if face.size == 0:
                continue
            face_encoding = extract_face_encoding(face)

            # Recognize face
            is_existing_user = recognize_face(face_encoding)

            if is_existing_user:
                return "Existing User ✅"
            else:
                # Save the new face encoding in the DB
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO faces (encoding) VALUES (?)", (face_encoding.tobytes(),))
                conn.commit()
                conn.close()
                return "New User ❌"

    return "Face not detected"
