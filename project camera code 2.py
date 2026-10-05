import os
import sys
import time

# Force TensorFlow to use the legacy Keras 2 engine.
# Teachable Machine exports Keras 2 models, which Keras 3 cannot load.
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# Block pyarrow so it cannot crash TensorFlow on import.
sys.modules["pyarrow"] = None

import cv2
import numpy as np
import serial
from tf_keras.models import load_model

# Find the model and labels next to this script, whatever folder you run it from
HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Serial settings
# ----------------------------------------------------------------------

# Which message to send for each label number in labels.txt.
# 1 peanutbuttersandwich -> "yellow"
# 2 cheezit              -> "red"
# 3 calculator           -> "blue"
MESSAGE_FOR_LABEL = {
    0: "red",   # cheez it
    1: "yellow",      # peanut butter sandwich
    2: "blue",     # calculator
    3: "clear",    # background (all lights off)
}

NAME_FOR_LABEL = {
    0: "cheez it",
    1: "peanut butter sandwich",
    2: "calculator",
    3: "background",
}
# Must match the Serial.begin() number in the Arduino sketch
BAUD_RATE = 9600

# Only act on a prediction the model is fairly sure about
CONFIDENCE_THRESHOLD = 0.80

# The port your board is plugged into (Arduino IDE > Tools > Port)
SERIAL_PORT = "COM3"

# Open the serial port. If it cannot be opened the program still runs,
# so you can test the camera and model without hardware.
board = None
try:
    board = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    # Opening the port resets the Arduino. Give it time to restart.
    time.sleep(2)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as error:
    print(f"Could not open {SERIAL_PORT}: {error}")
    print("Check Tools > Port in the Arduino IDE, and close the Serial Monitor.")


def send(message):
    """Send one message to the board, followed by a newline."""
    if board is None:
        return
    board.write((message + "\n").encode())
    print(f"Sent: {message}")


# ----------------------------------------------------------------------
# Model, labels, and camera
# ----------------------------------------------------------------------

model = load_model(os.path.join(HERE, "keras_model.h5"), compile=False)

# Each line looks like "0 background", so keep only the name.
with open(os.path.join(HERE, "labels.txt"), "r") as f:
    class_names = [line.strip().split(" ", 1)[1] for line in f if line.strip()]

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    sys.exit("Could not open the camera. Try VideoCapture(1), or allow camera access "
             "for VS Code in Settings > Privacy & security > Camera.")

print("Click the webcam window, then press Esc or q to quit (or Ctrl+C in the terminal).")

# Remember what we sent last, so we only send when the answer changes.
last_message = None

while True:
    ret, frame = camera.read()
    if not ret:
        print("Could not read a frame from the camera.")
        break

    # Crop the center square, like Teachable Machine does
    h, w = frame.shape[:2]
    size = min(h, w)
    top, left = (h - size) // 2, (w - size) // 2
    frame = frame[top:top + size, left:left + size]

    # Resize to 224 x 224 pixels
    frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", frame)

    # OpenCV uses BGR, the model was trained on RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize to the range -1 to 1
    image = (image / 127.5) - 1

    # Predict
    prediction = model.predict(image, verbose=0)
    index = np.argmax(prediction[0])
    class_name = NAME_FOR_LABEL.get(int(index), f"unknown ({index})")
    confidence_score = prediction[0][index]

    print(f"Class: {class_name}   Confidence Score: {confidence_score * 100:.0f} %")

    # Decide what to send. Low confidence means send nothing.
    message = None
    if confidence_score >= CONFIDENCE_THRESHOLD:
        message = MESSAGE_FOR_LABEL.get(int(index))

    # Send only when the message changes from the one before it
    if message is not None and message != last_message:
        send(message)
        last_message = message

    # Esc key (27) or q to exit. The webcam window must be clicked first.
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
if board is not None:
    send("clear")   # turn the lights off on the way out
    board.close()