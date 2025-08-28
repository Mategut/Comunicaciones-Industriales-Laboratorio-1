void setup() {
  Serial.begin(9600, SERIAL_8E1);        // UART: 9600 baudios, 8E1
  pinMode(13, OUTPUT);       // LED verde (Arduino)
  pinMode(12, OUTPUT);       // LED rojo (Arduino)
}

void loop() {
  // Envío de byte válido: '0' = 0x30 = 00110000
  uint8_t Letra = 'A';
  Serial.write(Letra);

  digitalWrite(13, HIGH);   // LED verde ON (dato válido enviado)
  delay(500);
  digitalWrite(13, LOW);

  // Envío de byte con error simulado: 0xC1 = 11000001
  byte errorByte = 0xC1;    
  Serial.write(errorByte);
  digitalWrite(12, HIGH);   // LED rojo ON (error simulado enviado)
  delay(500);
  digitalWrite(12, LOW);

  delay(1000);              // Pausa antes de repetir
}