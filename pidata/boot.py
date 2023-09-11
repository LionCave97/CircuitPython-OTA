import board
import digitalio
import time
import storage

# Create a digital input object for GP16 (replace with the appropriate pin for your board)
gp16_pin = digitalio.DigitalInOut(board.GP16)
gp16_pin.direction = digitalio.Direction.INPUT
gp16_pin.pull = digitalio.Pull.UP

if gp16_pin.value:
    storage.remount("/", readonly=False)
    print("Storage mounted as read/write.")
else:
    storage.remount("/", readonly=True)
    print("Storage mounted as read-only.")