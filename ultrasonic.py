from machine import Pin
import utime
trigger = Pin(13, Pin.OUT)
echo = Pin(12, Pin.IN)

def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = timepassed * (0.034 / 2)
   print(distance)
   
while True:
    ultra()