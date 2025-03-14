import cv2
import os
import urllib.request
import requests
import json

# Constants
MODEL_URLS = {
    "prototxt": "https://logeshm05.github.io/deploy.prototxt",
    "caffemodel": "https://logeshm05.github.io/res10_300x300_ssd_iter_140000_fp16.caffemodel"
}
CONFIDENCE_THRESHOLD = 0.5
BLOB_SIZE = (300, 300)

# Global model cache
caffe_model = None

def get_model_paths():
    base_dir = os.path.expanduser("~")
    model_dir = os.path.join(base_dir, "models")
    os.makedirs(model_dir, exist_ok=True)
    return {
        "prototxt": os.path.join(model_dir, "deploy.prototxt"),
        "caffemodel": os.path.join(model_dir, "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    }

def download_model():
    paths = get_model_paths()
    for key, path in paths.items():
        if not os.path.exists(path):
            try:
                print(f"Downloading {key} model...")
                urllib.request.urlretrieve(MODEL_URLS[key], path)
            except Exception as e:
                print(f"❌ Failed to download {key}: {e}")
    return paths["prototxt"], paths["caffemodel"]

def load_caffe_model():
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

def detect_faces(image_path):
    print(f"✅ Python connected")

    net = load_caffe_model()
    if net is None:
        return "Model loading failed."

    image = cv2.imread(image_path)
    if image is None:
        return "Image not found."

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=BLOB_SIZE,
                                 mean=(104.0, 177.0, 123.0), swapRB=False, crop=False)
    net.setInput(blob)
    detections = net.forward()

    face_count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONFIDENCE_THRESHOLD:
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
    url = "http://172.31.3.151:5005/recognize"
    try:
        with open(image_path, 'rb') as image_file:
            files = {"image": (os.path.basename(image_path), image_file, "image/jpeg")}
            headers = {"Accept": "application/json"}
            response = requests.post(url, files=files, headers=headers)
            print(f"✅ API Response: {response.text}")
            json_response = response.json()
            # json_response["image_path"] = image_path
            return json_response
    except Exception as e:
        print(f"❌ Error sending image to API: {e}")
        return {"error": "API request failed.", "message": str(e)}

def send_image_to_server(image_path):
    url = "http://172.31.3.151:5005/upload"
    try:
        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            response = requests.post(url, files=files)
        return response.text
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return str(e)
