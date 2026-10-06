nt yellowLed = 8;
int redLed = 7;
int blueLed = 6;
int buzzer = 9;

void allOff() {
  digitalWrite(yellowLed, LOW);
  digitalWrite(redLed, LOW);
  digitalWrite(blueLed, LOW);
  noTone(buzzer);
}

void beep(int freq, int times) {
  for (int i = 0; i < times; i++) {
    tone(buzzer, freq);
    delay(150);
    noTone(buzzer);
    delay(100);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(yellowLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(blueLed, OUTPUT);
  pinMode(buzzer, OUTPUT);
  allOff();
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == "yellow")     { allOff(); digitalWrite(yellowLed, HIGH); beep(1000, 1); }
    else if (msg == "red")   { allOff(); digitalWrite(redLed, HIGH);    beep(600, 2); }
    else if (msg == "blue")  { allOff(); digitalWrite(blueLed, HIGH);   beep(1500, 3); }
    else if (msg == "clear") { allOff(); }
  }
}
