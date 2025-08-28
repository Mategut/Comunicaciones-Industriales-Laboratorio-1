from machine import Pin, UART
import time

# Configura LEDs externos
led_verde = Pin(13, Pin.OUT)  # LED verde (dato válido)
led_rojo = Pin(21, Pin.OUT)   # LED rojo (error paridad)

# Configura UART (UART0: GP0=TX, GP1=RX)
uart = UART(0, baudrate=9600, bits=8, parity=1, stop=1)

try:
    while True:
        if uart.any():  # Si hay datos en el buffer
            data = uart.read(1)   # Leer 1 byte
            if data:
                byte_val = data[0]  # Convierte a entero (0-255)
                ones = bin(byte_val).count("1")
                is_valid = (ones % 2 == 0)  # Paridad par: nº de 1's debe ser par

                if is_valid:
                    led_verde.value(1)
                    print("Dato valido:", data)
                else:
                    led_rojo.value(1)
                    print("Error de paridad! Byte:", hex(byte_val))

                time.sleep(0.5)
                led_verde.value(0)
                led_rojo.value(0)

except KeyboardInterrupt:
    led_verde.value(0)
    led_rojo.value(0)
    print("Programa detenido")
