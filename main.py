
from machine import Pin
from utime import sleep_ms

import actuators
import sensors
from robot import Robot


def run(robot):
    """Main pipeline for the robot."""
    robot.update()


button = Pin(14, Pin.IN, Pin.PULL_UP)

left_motor = actuators.Motor(6, 7)
right_motor = actuators.Motor(4, 5)

forklift_servo = actuators.Servo(Pin(15), 0)
claw_servo = actuators.Servo(Pin(16), 0)

left_light_sensor = sensors.Light_Sensor("GP10")
right_light_sensor = sensors.Light_Sensor("GP11")
far_left_light_sensor = sensors.Light_Sensor("GP12")
far_right_light_sensor = sensors.Light_sensor("GP13")

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

running = False
robot.off()

while True:
    if button.value() == 0:
        sleep_ms(30)  # Debounce

        if button.value() == 0:
            running = not running

            if not running:
                robot.reset()

            # Wait for button release
            while button.value() == 0:
                sleep_ms(10)

    if running:
        try:
            run(robot)
        except Exception as e:
            print("Robot error:", e)
            running = False
            robot.reset()

    sleep_ms(10)