
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
    '''
    navigator.get_route_for_box_state(has_box=False)
    navigator.FollowRoute()
    navigator.get_route_for_box_state(has_box=True)
    navigator.FollowRoute()
    '''
    #return robot.Forward_Until_Node(speed=100)
    robot.move_to_box(speed=50)
    
    #robot.test_light_sensors()
    return True

 

button = Pin("GP21", Pin.IN, Pin.PULL_DOWN)
running = False


robot_kwargs = {
    "one_eighty_degree_turn_range": [1000, 1500],  # time in ms for robot to turn 180 degrees
    "ninety_degree_turn_range": [600, 1200],  # time in ms for robot to turn 90 degrees
    "motor_correction": 20,  # Amount to adjust motor speed for line following
    "turning_sleep_time": 370,  # Sleep time during turning actions
    "reverse_turning_sleep_time": 250,  # Sleep time during reverse turning actions
    "control_frequency": 50,  # Control frequency in Hz
    "claw_close_angle": 22,
    "forklift_default_angle": 108,
    "claw_open_angle": 110,  # 
    "forklift_lower_angle": 0,
    "forklift_raise_angle": 200,
    "collection_time": 50000,
    "left_motor_bias": 15,  # Amount to adjust left motor speed for line following
    "right_motor_bias": 0,  # Amount to adjust right motor speed for line following
}


left_motor = actuators.Motor(7, 6, correction=robot_kwargs["left_motor_bias"])
right_motor = actuators.Motor(4, 5, correction=robot_kwargs["right_motor_bias"])

forklift_servo = actuators.Servo(Pin(15))
claw_servo = actuators.Servo(Pin(13))



left_light_sensor = sensors.Light_Sensor("GP12")
right_light_sensor = sensors.Light_Sensor("GP8")
far_left_light_sensor = sensors.Light_Sensor("GP10")
far_right_light_sensor = sensors.Light_Sensor("GP11")



led_red = leds.LED("GP22")
led_green = leds.LED("GP27")
led_yellow = leds.LED("GP26")

led_red.off()
led_green.off()
led_yellow.on()



#magnetometer = None
magnetometer = sensors.Magnetometer(Pin("GP28"))

dropoff_distance_sensor = sensors.Distance_Sensor(sda=16, scl=17, config=0)
collection_distance_sensor = sensors.Distance_Sensor(sda=18, scl=19, config=1)
#dropoff_distance_sensor = None
#collection_distance_sensor = None




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
    dropoff_distance_sensor=dropoff_distance_sensor,
    led_red=led_red,
    led_yellow=led_yellow,
    led_green=led_green
    )

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
            '''
            except Exception as e:
                print("Robot error:", e)
                running = False
                robot.reset()
            '''
            sleep_ms(10)
    finally:
        robot.reset()
