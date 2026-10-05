int yellowLed = 8;
int redLed = 7;
int blueLed = 6;

void allOff() {
  digitalWrite(yellowLed, LOW);
  digitalWrite(redLed, LOW);
  digitalWrite(blueLed, LOW);
}

void setup() {
  Serial.begin(9600);   // must match BAUD_RATE in demo.py
  pinMode(yellowLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(blueLed, OUTPUT);
  allOff();
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == "yellow")     { allOff(); digitalWrite(yellowLed, HIGH); }
    else if (msg == "red")   { allOff(); digitalWrite(redLed, HIGH); }
    else if (msg == "blue")  { allOff(); digitalWrite(blueLed, HIGH); }
    else if (msg == "clear") { allOff(); }
  }
}