import max7219
from machine import Pin, SPI

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 1)
display.brightness(3)
display.text('9', 0, 0, 1)
display.show()