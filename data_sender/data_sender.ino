void setup() {
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Read the analog value from pin A0
  int sensorValue = analogRead(A0);

  // Send the sensor value to the Serial Plotter
  Serial.println(sensorValue);

  // Add a small delay to control the data rate
  delay(1); // Adjust this delay as needed
}
