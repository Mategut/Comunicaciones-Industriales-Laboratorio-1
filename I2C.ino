#include <Wire.h>

volatile byte ultimoDato = 0;   // compartido entre loop() e ISR

void setup() {
  // Si quieres depurar por Serial, hazlo solo en loop()
  Serial.begin(115200);

  Wire.begin(0x08);             // Esclavo I2C en 0x08
  Wire.onRequest(ReadValue);    // Callback rápido: solo Wire.write(...)
}

void loop() {
  // Leer potenciómetro en tiempo normal (NO en la ISR)
  int valor = analogRead(A0);                   // 0..1023
  byte dato = (byte)map(valor, 0, 1023, 0, 7);  // 0..7 para 3 LEDs
  ultimoDato = dato;                            // actualizar valor compartido

  // Depuración (opcional) SOLO aquí
  static unsigned long t0 = 0;
  if (millis() - t0 > 500) {
    t0 = millis();
    Serial.print(F("Ultimo dato: "));
    Serial.println(ultimoDato);
  }
}

void ReadValue() {
  // ISR I2C: debe ser MUY breve. Nada de analogRead/Serial/delays.
  Wire.write(ultimoDato);
}