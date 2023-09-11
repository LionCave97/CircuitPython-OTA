import time
import board
import digitalio

# update code!
from autoupdate import AutoUpdate
last_update = time.monotonic()
AutoUpdate()

# Main code! 
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    current_time = time.monotonic()
    print(current_time - last_update)
    if current_time - last_update >= 600:  # 600 seconds = 10 minutes
        AutoUpdate()
        last_update = current_time

    print("Hello world!")
    time.sleep(1)
    led.value = True
    time.sleep(2)
    led.value = False