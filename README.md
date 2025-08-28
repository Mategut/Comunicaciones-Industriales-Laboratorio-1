# Laboratorio 1. Comunicación Arduino – Raspberry Pi Pico

Este repositorio contiene el informe y el código fuente desarrollado en el laboratorio de comunicación entre Arduino Uno y Raspberry Pi Pico mediante tres protocolos clásicos: UART, SPI e I²C.  
El proyecto incluye tanto el documento en LaTeX con formato IEEE como los programas en Arduino y Raspberry Pi Pico, junto con imágenes de resultados experimentales.

---

##  Comunicación UART
En este punto se estableció una comunicación serie asíncrona entre Arduino y Raspberry Pi Pico usando UART.  
El Arduino envía bytes con y sin error de paridad, mientras que la Raspberry Pi Pico verifica los datos recibidos y enciende un **LED verde** si la transmisión fue correcta o un **LED blanco** si hubo error.
En los programas presentados, tanto en Arduino como en la Raspberry Pi Pico, se observa un correcto funcionamiento básico de envío y verificación de datos UART. Ambos cumplen con su propósito, pero existen oportunidades de mejora:

- Arduino
  - Evitar duplicación de código encapsulando el envío de bytes en funciones.  
  - Usar constantes para los pines de LEDs.  
  - Reemplazar `delay()` por `millis()` para un enfoque no bloqueante.  

- Raspberry Pi Pico
  - Implementar una función dedicada a la verificación de paridad.  
  - Usar `.on()` y `.off()` para mayor claridad en el control de LEDs.  
  - Declarar constantes para pines y parámetros UART.  
  - Extender con un conteo de bytes válidos/erróneos o registro histórico.  

---

## Comunicación SPI
En esta práctica se utilizó SPI, donde la Raspberry Pi Pico actuó como maestro y el Arduino como esclavo.  
El maestro envía comandos para encender y apagar un LED en el Arduino, y el esclavo responde con un código de confirmación. Los resultados se visualizaron tanto en consola como en el montaje físico.
En la implementación de comunicación SPI entre la Raspberry Pi Pico (maestro) y el Arduino (esclavo) se logra un intercambio funcional de comandos para encender y apagar un LED, con confirmación en consola. Mejoras posibles:

- Raspberry Pi Pico
  - Declarar constantes para comandos y respuestas (`CMD_ON`, `CMD_OFF`).  
  - Validar la respuesta recibida en lugar de solo imprimirla.  
  - Organizar el envío de comandos en funciones genéricas, pensando en escalabilidad.  

- Arduino
  - Definir comandos como constantes o enumeraciones para mayor claridad.  
  - Encapsular el manejo de comandos en funciones separadas.  
  - Incluir un manejo explícito de errores (comandos inválidos).  

---

## Comunicación I²C
En este ejercicio se implementó I²C para transmitir desde Arduino (esclavo) el valor de un potenciómetro hacia la Raspberry Pi Pico (maestro).  
El valor leído se redujo a 3 bits y se mostró en tres LEDs conectados a la Pi, encendiéndose en función del nivel del potenciómetro. También se imprimieron los datos en la consola.
En este ejercicio se establece comunicación I²C entre Arduino (esclavo) y Raspberry Pi Pico (maestro) para leer un potenciómetro y representar sus 3 bits más significativos en LEDs.

- Arduino
  - Declarar constantes para dirección I²C y rangos de conversión.  
  - Proteger la variable compartida entre ISR y loop.  
  - Documentar mejor el mapeo del potenciómetro (0–7) hacia LEDs.  

- Raspberry Pi Pico
  - Encapsular la lógica de encendido de LEDs en una función genérica.  
  - Definir constantes para dirección del esclavo, frecuencia y tiempos.  
  - Implementar reconexión automática en caso de error de comunicación.  

---

Trabajo realizado por:  
- Mateo Gutiérrez  
- Julián Montealegre  
- Nicolás Alfonso  
