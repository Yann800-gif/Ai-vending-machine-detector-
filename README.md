# Snack Detector: AI-Hardware Pipeline

A camera watches an object, a vision model I trained myself recognizes it, and an Arduino lights an LED of a matching color.

| Object shown | LED that lights up |
|---|---|
| Cheez-It | Yellow |
| Peanut butter sandwich | Red |
| Calculator | Blue |
| Nothing (background) | All LEDs off |

## How the pipeline works

1. **Camera:** OpenCV captures a frame from the webcam, crops the center square, and resizes it to 224x224.
2. **Model:** a Keras image classifier trained in Google Teachable Machine predicts which object is in view.
3. **Serial:** if the confidence is 80% or higher, Python sends a text message (`yellow`, `red`, `blue`, or `clear`) to the Arduino over USB. It only sends when the prediction changes.
4. **Arduino:** the sketch reads the message and turns on the matching LED (one at a time).

```
Webcam -> Python + trained model -> USB serial -> Arduino Mega 2560 -> LED
```

## Hardware

- Arduino Mega 2560 (USB cable)
- Breadboard and jumper wires
- 3 LEDs (yellow, red, blue)
- 3 resistors (220 ohm)
- Laptop with a webcam

### Pin map

| Part | Arduino pin |
|---|---|
| Yellow LED (Cheez-It) | 8 |
| Red LED (peanut butter sandwich) | 7 |
| Blue LED (calculator) | 6 |
| Ground | GND to the breadboard - rail |

Each LED: pin to the long leg (+), short leg through a 220 ohm resistor to the GND rail.

## Model

Trained by me in Google Teachable Machine (Image Project), exported as Keras.

`labels.txt`:

```
0 cheez it
1 peanutsandwich
2 calculator
3 background
```

The background class (empty scene, hands, face) maps to `clear`, so all LEDs turn off when nothing is shown.

## Files

```
snack_detector.py                         Python: camera, model, serial
snack_detector_sketch/
    snack_detector_sketch.ino             Arduino sketch
keras_model.h5                            Trained model
labels.txt                                Class labels
```

## How to run

1. Install the Python packages:
   ```
   pip install tensorflow tf_keras opencv-python numpy pyserial
   ```
2. Open `snack_detector_sketch.ino` in the Arduino IDE. Select **Tools > Board > Arduino Mega or Mega 2560** and the correct **Port**, then click **Upload**.
3. Close the Arduino IDE Serial Monitor (only one program can use the port at a time).
4. In `snack_detector.py`, set `SERIAL_PORT` to your port (for example `COM3`).
5. Run:
   ```
   python snack_detector.py
   ```
6. Hold up each object in the center of the camera view. Click the webcam window and press `q` or Esc to quit.

## Problems I ran into and how I fixed them

*(Edit this section in your own words and add anything else you remember.)*

- **Wrong pin:** my LED was on pin 11, but the sketch used pin 13. I tested the LED with the Blink example to find the right pin.
- **COM3 "Access is denied":** a running Python script (or the Serial Monitor) was holding the port, so uploads failed. I had to stop Python before every upload.
- **Label numbers start at 0:** Teachable Machine shows classes starting at 1, but `labels.txt` starts at 0. The mapping in the code has to use the `labels.txt` numbers.
- **Labels in a different order:** after retraining, my classes were in a different order than I expected, so the terminal showed the wrong names. I fixed the mapping to match `labels.txt`.
- **Arduino code saved as `.py`:** VS Code underlined everything. Arduino code must be saved as `.ino` in a folder with the same name.
- **LED stayed on when nothing was shown:** the first model had no background class, so it always picked one of the three objects. I added a background class in Teachable Machine, retrained, and mapped it to `clear` so all LEDs turn off.
- **Camera script kept running:** the `q` key only works when the webcam window is selected, so I used Ctrl+C or the terminal trash can when needed.

## Photos and video

*(Add your pictures or video here, for example:)*

- `images/circuit.jpg`: the breadboard and Arduino
- `images/demo.mp4`: the demo working with each object

## Possible improvements

- Add a buzzer with a different beep per object.
