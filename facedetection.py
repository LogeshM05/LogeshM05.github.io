import cv2
import os
import urllib.request
import requests

# URLs for downloading the model files
MODEL_URLS = {
    "prototxt": "https://logeshm05.github.io/deploy.prototxt",
    "caffemodel": "https://logeshm05.github.io/res10_300x300_ssd_iter_140000_fp16.caffemodel"
}

# Global variable to store the model
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

def detect_faces(image_path):
    """Detects faces in an image using the loaded model and sends it to API."""
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

    face_count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            face_count += 1
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

    if face_count == 0:
        return "Face not detected"

    output_path = image_path.replace(".jpg", "_detected.jpg")
    cv2.imwrite(output_path, image)
    print(f"✅ Faces detected: {face_count}, saved at {output_path}")

    return face_recognition_api(output_path)

def face_recognition_api(image_path):
    """Sends the processed image to the face recognition API."""
    url = "http://172.31.3.188:5000//recognize"
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {"image": (os.path.basename(image_path), image_file, "image/jpeg")}
            response = requests.post(url, files=files)
            print(f"✅ API Response: {response.text}")
            return response.text
    except Exception as e:
        print(f"❌ Error sending image to API: {e}")
        return "API request failed."

# Example usage
# detect_faces("path/to/your/image.jpg")
