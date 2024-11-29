
#define LedPin 27

void setup() {
  pinMode(LedPin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  delay(10);
  digitalWrite(LedPin, HIGH);
  delay(10);
  digitalWrite(LedPin, LOW);

}
