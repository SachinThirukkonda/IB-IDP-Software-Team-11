
from machine import Pin
from utime import sleep_ms

import actuators
import sensors
import leds
from robot import Robot
from Navigation import Navigator
import Navigation as m


def run(robot):
    """Main pipeline for the robot."""
    #navigator.get_route_for_box_state(has_box=False)
    #navigator.get_route_for_box_state(has_box=True)

    return robot.test_light_sensors()
    
    return True

    

button = Pin("GP21", Pin.IN, Pin.PULL_DOWN)
running = False

left_motor = actuators.Motor(7, 6)
right_motor = actuators.Motor(4, 5)

forklift_servo = actuators.Servo(Pin("GP13"), 0)
claw_servo = actuators.Servo(Pin("GP15"), 0)

left_light_sensor = sensors.Light_Sensor("GP12")
right_light_sensor = sensors.Light_Sensor("GP8")
far_left_light_sensor = sensors.Light_Sensor("GP10")
far_right_light_sensor = sensors.Light_Sensor("GP11")


#led_red = leds.LED("GP4")
#led_green = leds.LED("GP2")
#led_yellow = leds.LED("GP3")


led_red = None
led_green = None
led_yellow = None

magnetometer = sensors.Magnetometer(Pin("GP28"))

#collection_distance_sensor = sensors.Distance_Sensor(sda=16, scl=17)
#dropoff_distance_sensor = sensors.Distance_Sensor(19, 20)
dropoff_distance_sensor = None
collection_distance_sensor = None

robot_kwargs = {
    "one_eighty_degree_turn_range": [1000, 1500],  # time in ms for robot to turn 180 degrees
    "ninety_degree_turn_range": [500, 700],  # time in ms for robot to turn 90 degrees
    "motor_correction": 25,  # Amount to adjust motor speed for line following
    "turning_sleep_time": 250,  # Sleep time during turning actions
    "reverse_turning_sleep_time": 250,  # Sleep time during reverse turning actions
    "control_frequency": 50,  # Control frequency in Hz
    "claw_close_angle": 10,
    "forklift_default_angle": 108,
    "claw_open_angle": 45,  # 
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
    collection_distance_sensor=collection_distance_sensor,
    dropoff_distance_sensor=dropoff_distance_sensor
    )
navigator = Navigator(robot=robot, strt = m.strt)

'''

while running:
            try:
                running = run(robot)
            except Exception as e:
                print("Robot error:", e)
                running = False
                robot.reset()
            sleep_ms(10)
robot.reset()

'''


while True:
    if button.value() == 1 and running == False:
        print("Button pressed. Starting robot.")
        #robot.led_yellow.start_flash()
        sleep_ms(1000)  # Debounce delay
        running = True
        
    if button.value() == 1 and running == True:
        print("Button pressed. Stopping robot.")
        #robot.led_yellow.stop_flash()
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