import cv2
import matplotlib.pyplot as plt
import urllib.request
import os
from time import time

def download_file(url, destination):
    """Downloads a file from a URL if it doesn't exist."""
    if not os.path.exists(destination):
        print(f"Downloading {url}...")
        try:
            urllib.request.urlretrieve(url, destination)
            print(f"Downloaded: {destination}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            exit(1)

def download_model():
    """Ensures the required Caffe model files are available."""
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    
    prototxt_url = "https://logeshm05.github.io/deploy.prototxt"
    caffemodel_url = "https://logeshm05.github.io/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    
    prototxt_path = os.path.join(model_dir, "deploy.prototxt")
    caffemodel_path = os.path.join(model_dir, "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    
    download_file(prototxt_url, prototxt_path)
    download_file(caffemodel_url, caffemodel_path)
    print("download model successfully")
    
    return prototxt_path, caffemodel_path

def load_caffe_model():
    """Loads the Caffe model for face detection."""
    prototxt, caffemodel = download_model()
    model = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
    return model

def cvDnnDetectFaces(image, opencv_dnn_model, min_confidence=0.5, display=True):
    """Detects faces in an image using OpenCV DNN model."""
    image_height, image_width, _ = image.shape
    output_image = image.copy()
    
    preprocessed_image = cv2.dnn.blobFromImage(
        image, scalefactor=1.0, size=(300, 300),
        mean=(104.0, 117.0, 123.0), swapRB=False, crop=False
    )
    
    opencv_dnn_model.setInput(preprocessed_image)
    start = time()
    results = opencv_dnn_model.forward()
    end = time()
    
    for face in results[0][0]:
        face_confidence = face[2]
        if face_confidence > min_confidence:
            bbox = face[3:]
            x1 = int(bbox[0] * image_width)
            y1 = int(bbox[1] * image_height)
            x2 = int(bbox[2] * image_width)
            y2 = int(bbox[3] * image_height)
            
            cv2.rectangle(output_image, (x1, y1), (x2, y2), (0, 255, 0), image_width // 200)
            cv2.rectangle(output_image, (x1, y1 - image_width // 20), (x1 + image_width // 16, y1),
                          (0, 255, 0), -1)
            cv2.putText(output_image, str(round(face_confidence, 1)), (x1, y1 - 25), 
                        cv2.FONT_HERSHEY_COMPLEX, image_width // 700, (255, 255, 255), image_width // 200)
    
    if display:
        cv2.destroyAllWindows()
        plt.figure(figsize=[20, 20])
        plt.subplot(121); plt.imshow(image[:, :, ::-1]); plt.title("Original Image"); plt.axis('off')
        plt.subplot(122); plt.imshow(output_image[:, :, ::-1]); plt.title("Output"); plt.axis('off')
        plt.show()
    else:
        return output_image, results

def main():
    """Main function to execute face detection."""
    opencv_dnn_model = load_caffe_model()
    image = cv2.imread('media/test.jpg')
    if image is None:
        print("Error: Unable to load image.")
        return
    cvDnnDetectFaces(image, opencv_dnn_model, display=True)

if __name__ == "__main__":
    main()
