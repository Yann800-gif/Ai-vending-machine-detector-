# Snack Detector: AI-Hardware Pipeline

A prototype detector for an AI self-serve vending machine: a camera watches an object, a vision model I trained myself recognizes it, and an Arduino responds with a matching LED and beeps.

| Object shown | LED | Buzzer |
|---|---|---|
| Cheez-It | Red | 2 beeps |
| Peanut butter sandwich | Yellow | 1 beep |
| Calculator | Blue | 3 beeps |
| Nothing (background) | All LEDs off | Silent |

## How the pipeline works

1. **Camera:** OpenCV captures a frame from the webcam, crops the center square, and resizes it to 224x224.
2. **Model:** a Keras image classifier trained in Google Teachable Machine predicts which object is in view.
3. **Serial:** if the confidence is 80% or higher, Python sends a text message (`yellow`, `red`, `blue`, or `clear`) to the Arduino over USB. It only sends when the prediction changes.
4. **Arduino:** the sketch reads the message, turns on the matching LED (one at a time), and beeps the buzzer 1, 2, or 3 times.

```
Webcam -> Python + trained model -> USB serial -> Arduino Mega 2560 -> LED + buzzer
```

## Hardware

- Arduino Mega 2560 (USB cable)
- Breadboard and jumper wires
- 3 LEDs (yellow, red, blue)
- 3 resistors (220 ohm)
- 1 buzzer
- Laptop with a webcam

### Pin map

| Part | Arduino pin |
|---|---|
| Red LED (Cheez-It) | 8 |
| Yellow LED (peanut butter sandwich) | 7 |
| Blue LED (calculator) | 6 |
| Buzzer (+ leg) | 9 |
| Ground | GND to the breadboard - rail (also the buzzer's - leg) |

Each LED: pin to the long leg (+), short leg through a 220 ohm resistor to the GND rail.
Buzzer: long (+) leg to pin 9, short (-) leg to GND.

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
project camera code 2.py        Python: camera, model, serial
9code/
    9code.ino                   Arduino sketch (LEDs + buzzer)
keras_model.h5                  Trained model
labels.txt                      Class labels
```

## How to run

1. Install the Python packages:
   ```
   pip install tensorflow tf_keras opencv-python numpy pyserial
   ```
2. Open `9code.ino` in the Arduino IDE. Select **Tools > Board > Arduino Mega or Mega 2560** and the correct **Port**, then click **Upload**.
3. Close the Arduino IDE Serial Monitor (only one program can use the port at a time).
4. In `project camera code 2.py`, set `SERIAL_PORT` to your port (for example `COM3`).
5. Run:
   ```
   python "project camera code 2.py"
   ```
6. Hold up each object in the center of the camera view. Click the webcam window and press `q` or Esc to quit.

## Problems I ran into and how I fixed them

- **Wrong pin:** my LED was not on the pin I expected, so I had my agent write an Arduino test script to check every pin and make sure each LED works.
- **Camera would not open:** the VS Code camera script couldn't open the camera or read a frame because the camera was still being used in the background. I closed the other process.
- **Classes in a different order:** after retraining, my classes were in a different order than I expected, so the terminal showed the wrong names. I fixed the mapping to match `labels.txt`.
- **Arduino code underlined in VS Code:** Arduino code must be saved as `.ino` in a folder with the same name, not as `.py`.
- **LED stayed on when nothing was shown:** the first model had no background class, so it always picked one of the three objects. I added a background class in Teachable Machine, retrained, and mapped it to `clear` so all LEDs turn off.
- **Camera script kept running:** the `q` key only works when the webcam window is selected, so I used Ctrl+C or the terminal trash can when needed.

## Photos and video

I have submitted all photos and videos.

## Possible improvements

- Add a servo that opens a "slot" for the detected snack.
- Add an LCD that shows the item name and price.
- Train on more snacks and in different lighting.
