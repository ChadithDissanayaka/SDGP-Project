from flask import Flask, jsonify, request
import cv2
from tensorflow import keras
import numpy as np

app = Flask(__name__)

# Load pre-trained model
model = keras.models.load_model('model.h5')

# Load Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route('/emotion-recognition', methods=['POST'])
def recognize_emotion():
    # Read video stream from client
    img_bytes = request.files['video'].read()
    nparr = np.fromstring(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Iterate through each face and predict emotion
    results = []
    for (x, y, w, h) in faces:
        # Crop face region
        face = gray[y:y+h, x:x+w]

        # Resize face to match input size of model
        face = cv2.resize(face, (48, 48))

        # Normalize pixel values
        face = face / 255.0

        # Reshape to match input shape of model
        face = face.reshape(1, 48, 48, 1)

        # Predict emotion using model
        emotion = model.predict(face)[0]

        # Map predicted probabilities to emotion labels
        emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        emotion_label = emotions[np.argmax(emotion)]

        # Add emotion result to results list
        results.append({'x': x, 'y': y, 'w': w, 'h': h, 'emotion': emotion_label})

    # Return results as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run()
