
from machine import Pin
from utime import sleep_ms

import actuators
import sensors
from robot import Robot


def run(robot):
    """Main pipeline for the robot."""
    robot.update()


#button = Pin("GP22", Pin.IN, Pin.PULL_DOWN)

left_motor = actuators.Motor(7, 6)
right_motor = actuators.Motor(4, 5)

forklift_servo = actuators.Servo(Pin("GP15"), 0)
claw_servo = actuators.Servo(Pin("GP15"), 0)

left_light_sensor = sensors.Light_Sensor("GP11")
right_light_sensor = sensors.Light_Sensor("GP12")

far_left_light_sensor = sensors.Light_Sensor("GP10")
far_right_light_sensor = sensors.Light_Sensor("GP13")

robot = Robot(
    left_motor=left_motor,
    right_motor=right_motor,
    forklift_servo=forklift_servo,
    claw_servo=claw_servo,
    left_light_sensor=left_light_sensor,
    right_light_sensor=right_light_sensor,
    far_left_light_sensor=far_left_light_sensor,
    far_right_light_sensor=far_right_light_sensor
    )

try:
    while True:
        try:
            run(robot)
        except Exception as e:
            print("Robot error:", e)
            running = False
            robot.reset()
        sleep_ms(10)
finally:
    print("Program ended")
    robot.reset()