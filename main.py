
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
    return True

button = Pin("GP21", Pin.IN, Pin.PULL_DOWN)
running = False

robot_kwargs = {
    "one_eighty_degree_turn_range": [1000, 1500],   # time in ms for robot to turn 180 degrees
    "ninety_degree_turn_range": [600, 1200],        # time in ms for robot to turn 90 degrees
    "motor_correction": 20,                         # Amount to adjust motor speed for line following
    "turning_sleep_time": 370,                      # Sleep time during turning actions
    "reverse_turning_sleep_time": 340,              # Sleep time during reverse turning actions
    "control_frequency": 50,                        # Control frequency in Hz
    "claw_close_angle": 22,                         # Close angle for claw
    "forklift_default_angle": 108,                  # Default raise angle for transportation of box
    "claw_open_angle": 110,                         # Open angle for claw
    "forklift_lower_angle": 0,                      # Lower angle for forklift when collecting box
    "forklift_raise_angle": 194,                    # Raise angle for forklift when dropping off box
    "collection_time": 50000,                       # Time in ms to wait for box collection
    "left_motor_bias": 0,                           # Amount to adjust left motor speed for line following
    "right_motor_bias": 0,                          # Amount to adjust right motor speed for line following
    "speed": 80,                                    # Default speed for robot movement
    "turning_speed": 80,                            # Speed for turning actions
}

# Adjust timing parameters proportionally based on speed
robot_kwargs["turning_sleep_time"] = int(robot_kwargs["turning_sleep_time"] * 100 / robot_kwargs["speed"])
robot_kwargs["reverse_turning_sleep_time"] = int(robot_kwargs["reverse_turning_sleep_time"] * 100 / robot_kwargs["speed"])
robot_kwargs["one_eighty_degree_turn_range"] = [int(t * 100 / robot_kwargs["turning_speed"]) for t in robot_kwargs["one_eighty_degree_turn_range"]]
robot_kwargs["ninety_degree_turn_range"] = [int(t * 100 / robot_kwargs["turning_speed"]) for t in robot_kwargs["ninety_degree_turn_range"]]


# Initialize motors
left_motor = actuators.Motor(7, 6, correction=robot_kwargs["left_motor_bias"])
right_motor = actuators.Motor(4, 5, correction=robot_kwargs["right_motor_bias"])

# Initialize servos
forklift_servo = actuators.Servo(Pin(15))
claw_servo = actuators.Servo(Pin(13))

# Initialize light sensors
left_light_sensor = sensors.Light_Sensor("GP12")
right_light_sensor = sensors.Light_Sensor("GP8")
far_left_light_sensor = sensors.Light_Sensor("GP10")
far_right_light_sensor = sensors.Light_Sensor("GP11")

# Initialize LEDs
led_red = leds.LED("GP22")
led_green = leds.LED("GP27")
led_yellow = leds.LED("GP26")

# Set initial LED states
led_red.off()
led_green.off()
led_yellow.on()

# Initialize magnetometer
magnetometer = sensors.Magnetometer(Pin("GP28"))

# Initialize distance sensors
dropoff_distance_sensor = sensors.Distance_Sensor(sda=16, scl=17, config=0)
collection_distance_sensor = sensors.Distance_Sensor(sda=18, scl=19, config=1)

# Initialize robot
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
    led_yellow=led_yellow, led_red=led_red, led_green=led_green,
    collection_distance_sensor=collection_distance_sensor,
    dropoff_distance_sensor=dropoff_distance_sensor
    )

# Initialize Navigator
navigator = Navigator(robot=robot, strt = m.strt)

while True:
    if button.value() == 1 and running == False:
        print("Button pressed. Starting robot.")
        led_yellow.start_flash()
        sleep_ms(1000)  # Debounce delay
        running = True
        
    if button.value() == 1 and running == True:
        print("Button pressed. Stopping robot.")
        led_yellow.stop_flash()
        sleep_ms(1000)  # Debounce delay
        running = False
        
    try:
        while running:
            running = run(robot)
            # Sleep to prevent high refresh rate of the loop, which can cause issues with the robot's operation / damage sensors
            sleep_ms(10)
    finally:
        robot.reset()
