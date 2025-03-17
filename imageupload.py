import requests

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
