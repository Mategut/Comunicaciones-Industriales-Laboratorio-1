#include <SPI.h>

#define LED_PIN 9

/*
SPI0: 
  # sck  (Clock)                  = GP18 => Pin 13 
  # mosi (Master Out - Slave in)  = GP19 => Pin 11
  # miso (Master In - Slave Out)  = GP16 <= Voltage Divider <= Pin 12
  # SS   (Slave Select)           = GP17 => Pin 10
  # GND  (Ground)                 = GND <=> GND
  # Led                           = Pin 9
*/
volatile byte command = 0;
volatile bool received = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);

  // Configurar Arduino como esclavo
  pinMode(MISO, OUTPUT);   // El esclavo solo puede mandar por MISO
  SPCR |= _BV(SPE);        // Habilita SPI en modo esclavo
  SPI.attachInterrupt();   // Habilita interrupción SPI
}

ISR(SPI_STC_vect) {
  command = SPDR;          // Leer byte recibido
  received = true;
}

void loop() {
  if (received) {
    byte response = 0;

    if (command == 0x01) {
      digitalWrite(LED_PIN, HIGH);
      response = 0xAA; // Ack encendido
    } 
    else if (command == 0x00) {
      digitalWrite(LED_PIN, LOW);
      response = 0x55; // Ack apagado
    }
    else {
      response = 0xFF; // Comando inválido
    }

    SPDR = response;   // Cargar respuesta → Maestro la recibe en el próximo ciclo
    received = false;
  }
}
