from utime import sleep_ms, ticks_ms
from helper import line_detection
class Robot:
    def __init__(self, left_motor, right_motor, forklift_servo, claw_servo, left_light_sensor, right_light_sensor, far_left_light_sensor, far_right_light_sensor):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.forklift_servo = forklift_servo
        self.claw_servo = claw_servo

        self.left_light_sensor = left_light_sensor
        self.right_light_sensor = right_light_sensor
        
        self.far_left_light_sensor = far_left_light_sensor
        self.far_right_light_sensor = far_right_light_sensor

        self.far_left_light_sensor = far_left_light_sensor
        self.far_right_light_sensor = far_right_light_sensor

        self.one_eighty_degree_turn_time = 1000  # time in ms for robot to turn 180 degrees
        self.ninety_degree_turn_time = 500  # time in ms for robot to turn 90 degrees

        self.has_box = False
    
    def Drive_forward(self, speed):
        self.left_motor.on(dir=1, speed=speed)
        self.right_motor.on(dir=1, speed=speed)

    def Line_Sensor_readings(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        far_left_line = self.far_left_light_sensor.value()
        far_right_line = self.far_right_light_sensor.value()
        return left_line, right_line, far_left_line, far_right_line
    
    def Line_following(self):
        left_line, right_line, _, _ = self.Line_Sensor_readings()
        if left_line == 0 and right_line == 1:
            print("Adjusting. Turning right.")
            self.right_motor.speed -= 20
        if left_line == 1 and right_line == 0:
            print("Adjusting. Turning left.")
            self.left_motor.speed -= 20
        self.left_motor.update()
        self.right_motor.update()
    
    def check_path(self):
        # Execute 90 degree turn if white detected on far sensors
        _, _, far_left_line, far_right_line = self.Line_Sensor_readings()

        if far_left_line == 0 and far_right_line == 1:
            return "right"

        elif far_left_line == 1 and far_right_line == 0:
            return "left"

        elif far_left_line == 1 and far_right_line == 1:
            # Update later for case where the robot is at a crossroads
            return "crossroads"
        else:
            return "straight"
    
    def turning_sequence(self, turn):
        # Buffer time to ensure robot doesn't turn at a crossroads
        # when moving at an angle to the line before the turn is executed.
        # Needs to be tested and adjusted for speed of robot
        sleep_ms(10)
        if self.check_path() == turn:
            # time for robot's wheels to reach the line before turning
            # needs to be tested and adjusted for speed of robot
            sleep_ms(0)
            if turn == "left":
                print("Executing left turn (tank drive)")
                self.right_motor.on(dir=1, speed=100)
                self.left_motor.on(dir=0, speed=100)
            if turn == "right":
                print("Executing right turn (tank drive)")
                self.left_motor.on(dir=1, speed=100)
                self.right_motor.on(dir=0, speed=100)
            # Turns for a set time or until line is detected again. 
            # rot_time is set as a safety in case the robot misses the line, to prevent it from continuing to turn indefinitely
            line_detection(self.ninety_degree_turn_time, self.left_light_sensor, self.right_light_sensor)

    def one_eighty_degree_turn(self):
        print("Executing 180 degree turn (tank drive)")
        self.left_motor.on(dir=1, speed=100)
        self.right_motor.on(dir=0, speed=100)
        # Buffer time for line detection to ensure the robot doesn't immediately detect the line before turning 180 degrees. 
        # Needs to be tested and adjusted for speed of robot
        sleep_ms(100)
        line_detection(self.one_eighty_degree_turn_time, self.left_light_sensor, self.right_light_sensor)

    def motion_control(self):
        self.Drive_forward(100)
        current_path = self.check_path()
        if current_path == "left" or current_path == "right":
            print(f"Detected a {current_path} turn.")
            self.turning_sequence(current_path)
        self.Line_following()
    
    def update(self):
        self.motion_control()
        # Control frequency of robot update loop to prevent overloading the CPU (set to 50 Hz)
        sleep_ms(20)
    
    def reset(self):
        self.left_motor.off()
        self.right_motor.off()
    
    def test_motors(self):
        print("Forward")
        self.left_motor.on(dir=1, speed=100)
        self.right_motor.on(dir=1, speed=100)

        sleep_ms(10)
        print("Reverse")
        self.left_motor.on(dir=0, speed=100)
        self.right_motor.on(dir=0, speed=100)
        sleep_ms(10)
    
    def test_servos(self):
        print("Move to 0°")
        self.forklift_servo.set_angle(0)
        self.claw_servo.set_angle(0)
        sleep_ms(2)

        print("Move to 135° (centre)")
        self.forklift_servo.set_angle(135)
        self.claw_servo.set_angle(135)
        sleep_ms(2)

        print("Move to 270°")
        self.forklift_servo.set_angle(270)
        self.claw_servo.set_angle(270)
        sleep_ms(2)
    
    def test_light_sensors(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        far_left_line = self.far_left_light_sensor.value()
        far_right_line = self.far_right_light_sensor.value()
        print(f"left_light_sensor: {left_line}, right_light_sensor: {right_line}, far_left_light_sensor: {far_left_line}, far_right_light_sensor: {far_right_line}")
        sleep_ms(100)
        

        
        
        
        
