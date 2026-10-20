# blinkatest.py
import board, digitalio

pin = digitalio.DigitalInOut(board.D21)
pin.direction = digitalio.Direction.INPUT
print("GPIO D21 set to INPUT – OK")
