import cv2
import os
import numpy as np
import sqlite3
import face_recognition
import uuid  # For generating unique user IDs

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
            id TEXT PRIMARY KEY,  -- Store UUID instead of auto-incremented ID
            encoding BLOB
        )
    """)
    conn.commit()
    conn.close()

def save_face_encoding(face_encoding):
    """Save face encoding with a generated unique ID in the database."""
    if face_encoding.shape[0] != 128:
        print(f"Invalid encoding shape: {face_encoding.shape}, skipping save.")
        return None  # Do not save invalid encodings
    
    user_id = str(uuid.uuid4())  # Generate a unique UUID
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faces (encoding) VALUES (?)", (encoding.tobytes(),))
    conn.commit()
    conn.close()

def load_stored_encodings():
    """Retrieve stored encodings from the database (Optimized)."""
    global stored_encodings
    if stored_encodings is None:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT encoding FROM faces")
        stored_encodings = [np.frombuffer(enc[0], dtype=np.float32) for enc in cursor.fetchall()]
        conn.close()
    return stored_encodings

def extract_face_encoding(image):
    """Extracts a 128-dimensional feature vector from a face using face_recognition."""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)
    return face_encodings[0] if face_encodings else None

def detect_and_recognize_faces(image_path):
    """Detects faces, extracts features, and assigns/retrieves unique user IDs."""
    image = cv2.imread(image_path)
    if image is None:
        return "Image not found."

    stored_encodings = load_stored_encodings()  # Load stored face encodings with IDs
    results = []

    # Convert the image to RGB for face recognition
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for face_encoding in face_encodings:
        if face_encoding.shape[0] != 128:
            print(f"Skipping invalid encoding: {face_encoding.shape}")
            continue  # Skip invalid encodings

        matched_user_id = None

        # Compare with stored encodings
        for user_id, stored_encoding in stored_encodings:
            if stored_encoding.shape[0] != 128:
                print(f"Skipping stored encoding with invalid shape: {stored_encoding.shape}")
                continue

            distance = np.linalg.norm(stored_encoding - face_encoding)
            if distance < 0.6:  # Face match threshold
                matched_user_id = user_id
                break  # Stop searching once a match is found

            is_existing_user = any(np.linalg.norm(stored - face_encoding) < 0.6 for stored in stored_encodings)

            if is_existing_user:
                results.append("Existing User ✅")
            else:
                save_face_encoding(face_encoding)
                results.append("New User ❌")

    return results if results else "Face not detected"

