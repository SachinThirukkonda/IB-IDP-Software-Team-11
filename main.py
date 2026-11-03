
from machine import Pin
import robot
from utime import sleep_ms

import actuators
import sensors
import leds
from robot import Robot
from Navigation import Navigator
import Navigation as m


def run(robot):
    """Main pipeline for the robot."""
    navigator.get_route_for_box_state(has_box=False)
    navigator.FollowRoute()
    navigator.get_route_for_box_state(has_box=True)
    navigator.FollowRoute()

    

button = Pin("GP21", Pin.IN, Pin.PULL_DOWN)
running = False

left_motor = actuators.Motor(7, 6)
right_motor = actuators.Motor(4, 5)

forklift_servo = actuators.Servo(Pin("GP13"), 0)
claw_servo = actuators.Servo(Pin("GP15"), 0)

left_light_sensor = sensors.Light_Sensor("GP8")
right_light_sensor = sensors.Light_Sensor("GP12")
far_left_light_sensor = sensors.Light_Sensor("GP11")
far_right_light_sensor = sensors.Light_Sensor("GP10")


led_red = leds.LED("GP4")
led_green = leds.LED("GP2")
led_yellow = leds.LED("GP3")


magnetometer = sensors.Magnetometer(Pin("GP28"))

#collection_distance_sensor = sensors.Distance_Sensor(sda=16, scl=17, config=0)
#dropoff_distance_sensor = sensors.Distance_Sensor(sda=14, scl=15, config=1)
dropoff_distance_sensor = None
collection_distance_sensor = None

robot_kwargs = {
    "one_eighty_degree_turn_range": [1000, 1500],  # time in ms for robot to turn 180 degrees
    "ninety_degree_turn_range": [500, 700],  # time in ms for robot to turn 90 degrees
    "motor_correction": 25,  # Amount to adjust motor speed for line following
    "turning_sleep_time": 250,  # Sleep time during turning actions
    "reverse_turning_sleep_time": 250,  # Sleep time during reverse turning actions
    "control_frequency": 50,  # Control frequency in Hz
    "claw_close_angle": 50,
    "forklift_default_angle": 108,
    "claw_open_angle": 110,  # 
    "forklift_lower_angle": 0,
    "forklift_raise_angle": 200,
    "collection_time": 5000
}

robot = Robot(
    parameters=robot_kwargs,
    left_motor=left_motor,
    right_motor=right_motor,
    forklift_servo=forklift_servo,
    claw_servo=claw_servo,
    left_light_sensor=left_light_sensor,
    right_light_sensor=right_light_sensor,
    far_left_light_sensor=far_left_light_sensor,
    far_right_light_sensor=far_right_light_sensor,
    magnetometer=magnetometer,
    led_green=led_green,
    led_red=led_red,
    led_yellow=led_yellow,
    collection_distance_sensor=collection_distance_sensor,
    dropoff_distance_sensor=dropoff_distance_sensor
    )
navigator = Navigator(robot=robot, strt = m.strt)

'''

while running:
            try:
                running = run(robot)
                #print("hello")
            except Exception as e:
                print("Robot error:", e)
                running = False
                robot.reset()
            sleep_ms(10)
robot.reset()

'''

led_yellow.on()
button_was_pressed = False

while True:
    button_pressed = button.value() == 1
    if button_pressed and not button_was_pressed:
        sleep_ms(50)  # Debounce the button press.
        if button.value() == 1:
            running = not running
            if running:
                print("Button pressed. Starting robot.")
                led_yellow.start_flash()
            else:
                print("Button pressed. Stopping robot.")
                led_yellow.stop_flash()
                robot.reset()

    button_was_pressed = button.value() == 1

    if running:
        try:
            run(robot)
        except Exception as e:
            print("Robot error:", e)
            robot.reset()
        running = False
        led_yellow.stop_flash()

    sleep_ms(10)
