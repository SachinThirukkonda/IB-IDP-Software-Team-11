from machine import Pin
from time import sleep
from test_motor import Motor

l_motor = Motor(dirPin=4, PWMPin=5)
r_motor = Motor(dirPin=4, PWMPin=5)
ls_left = Pin("GP10", Pin.IN, Pin.PULL_UP)
ls_right = Pin("GP11", Pin.IN, Pin.PULL_UP)
while True:
    print("Forward")
    l_motor.Forward(speed = 100)
    r_motor.Forward(speed = 100)
    lline = ls_left.value()
    rline = ls_right.value()
    print(f"ls_left: {lline}, ls_right: {rline}")
    if lline == 0 and rline == 1:
        print("Adjusting. Turning right.")
        l_motor.speed += 5
    if lline == 0 and rline == 1:
        print("Adjusting. Turning right.")
        l_motor.speed += 5
    sleep(0.2)