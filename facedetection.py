import cv2
import os
import numpy as np
import sqlite3
import face_recognition
import uuid  # For generating unique user IDs

# Define database path
DB_PATH = os.path.join(os.path.expanduser("~"), "face_database.db")

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
    cursor.execute("INSERT INTO faces (id, encoding) VALUES (?, ?)", (user_id, face_encoding.tobytes()))
    conn.commit()
    conn.close()
    return user_id

def load_stored_encodings():
    """Retrieve stored encodings along with their unique IDs from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, encoding FROM faces")
    
    stored_data = []
    for row in cursor.fetchall():
        encoding = np.frombuffer(row[1], dtype=np.float32)
        if encoding.shape[0] == 128:  # Ensure valid encoding
            stored_data.append((row[0], encoding))
        else:
            print(f"Skipping corrupted encoding for ID: {row[0]}")

    conn.close()
    return stored_data

def extract_face_encoding(image):
    """Extracts a 128-dimensional feature vector from a face using face_recognition."""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)
    
    if face_encodings:
        encoding = face_encodings[0]
        if encoding.shape[0] == 128:
            return encoding
        else:
            print(f"Unexpected encoding shape: {encoding.shape}, skipping.")
            return None
    return None

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

        if matched_user_id:
            results.append(f"User ID: {matched_user_id}")
        else:
            new_user_id = save_face_encoding(face_encoding)  # Save new encoding with UUID
            if new_user_id:
                results.append(f"New User ID: {new_user_id}")

    return results if results else "Face not detected"
