from machine import SPI, Pin
import time

# SPI0: 
    # sck  (Clock)                  = GP18 => Pin 13 
    # mosi (Master Out - Slave in)  = GP19 => Pin 11
    # miso (Master In - Slave Out)  = GP16 <= Voltage Divider <= Pin 12
    # SS   (Slave Select)           = GP17 => Pin 10
    # GND  (Ground)                 = GND <=> GND
    # Led                           = Pin 9

spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

cs = Pin(17, Pin.OUT)
cs.value(1)  # inactivo (alto)

commands = [0x01, 0x00]       # Encender y apagar LED

def Transfer(command):
    Buffer = bytearray(1)
    response = bytearray(1)
    Buffer[0] = command

    cs.value(0)
    spi.write_readinto(Buffer,response)
    cs.value(1)

    return response[0]


try:
    while True:
        response = Transfer(commands[0])
        print("Recibio =", hex(response))
        time.sleep(1)

        response = Transfer(commands[1])
        print("Recibio = ", hex(response))
        time.sleep(1)

except KeyboardInterrupt:
    spi.deinit()
    print("Finalizado")


