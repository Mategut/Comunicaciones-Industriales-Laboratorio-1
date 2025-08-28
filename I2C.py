from machine import Pin, I2C
from utime import sleep
import time

Led = Pin("LED", Pin.OUT)
Led.on()
i2c = I2C(0, scl = Pin(1), sda= Pin(0), freq = 100000)
print("Escaneando...")
print([hex(x) for x in i2c.scan()])
time.sleep(5)
ARDUINO_ADDR = 0x08

Leds = [Pin(18, Pin.OUT), Pin(19, Pin.OUT), Pin(20, Pin.OUT)] 

def LedsBinario(valor):
    for i in range(len(Leds)):
        Leds[i].value((valor >> i) & 1)

print("Program Started...")


while True:
    try:
        data = i2c.readfrom(ARDUINO_ADDR, 1)
        valor = data[0]
        print("Dato Recibido: ", valor)

        LedsBinario(valor)

        time.sleep(0.5)
        Led.toggle()

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Error I2C: ", e)
        time.sleep(1)

        
Led.off()
print("Finished.")
