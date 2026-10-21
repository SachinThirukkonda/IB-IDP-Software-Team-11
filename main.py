
from machine import Pin
from utime import sleep_ms

import actuators
import sensors
from robot import Robot
from Navigation import Navigator
import Navigation as m


def run(robot):
    """Main pipeline for the robot."""
    
    return robot.open_close()

button = Pin("GP21", Pin.IN, Pin.PULL_DOWN)
running = True

left_motor = actuators.Motor(7, 6)
right_motor = actuators.Motor(4, 5)

forklift_servo = actuators.Servo(Pin("GP15"), 0, 20)
claw_servo = actuators.Servo(Pin("GP15"), 0, 20)

left_light_sensor = sensors.Light_Sensor("GP11")
right_light_sensor = sensors.Light_Sensor("GP12")
far_left_light_sensor = sensors.Light_Sensor("GP10")
far_right_light_sensor = sensors.Light_Sensor("GP13")

magnetometer = sensors.Magnetometer(28)

robot_kwargs = {
    "one_eighty_degree_turn_range": [1000, 1500],  # time in ms for robot to turn 180 degrees
    "ninety_degree_turn_range": [500, 700],  # time in ms for robot to turn 90 degrees
    "motor_correction": 25,  # Amount to adjust motor speed for line following
    "turning_sleep_time": 500,  # Sleep time during turning actions
    "reverse_turning_sleep_time": 550,  # Sleep time during reverse turning actions
    "control_frequency": 50,  # Control frequency in Hz
    "claw_open_angle": 180,  # 
    "forklift_lower_angle": -120,
    "forklift_raise_angle": 45
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
    magnetometer=magnetometer)
navigator = Navigator(robot=robot, strt = m.strt)



while running:
            try:
                running = run(robot)
            except Exception as e:
                print("Robot error:", e)
                running = False
                robot.reset()
            sleep_ms(10)
while True:
    if button.value() == 1 and running == False:
        print("Button pressed. Starting robot.")
        sleep_ms(1000)  # Debounce delay
        running = True
        
    if button.value() == 1 and running == True:
        print("Button pressed. Stopping robot.")
        sleep_ms(1000)  # Debounce delay
        running = False    
        

    try:
        while running:
            try:
                running = run(robot)
            except Exception as e:
                print("Robot error:", e)
                running = False
                robot.reset()
            sleep_ms(10)
    finally:
        robot.reset()