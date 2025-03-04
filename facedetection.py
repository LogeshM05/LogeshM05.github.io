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
        return "Face not detected"  # Fixed indentation

    output_path = image_path.replace(".jpg", "_detected.jpg")
    cv2.imwrite(output_path, image)
