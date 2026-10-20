from utime import sleep_ms, ticks_ms
from helper import line_detection
class Robot:
    def __init__(self, left_motor, right_motor, forklift_servo, claw_servo, left_light_sensor, right_light_sensor, far_left_light_sensor, far_right_light_sensor, magnetometer=None):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.forklift_servo = forklift_servo
        self.claw_servo = claw_servo

        self.magnetometer = magnetometer

        self.left_light_sensor = left_light_sensor
        self.right_light_sensor = right_light_sensor
        
        self.far_left_light_sensor = far_left_light_sensor
        self.far_right_light_sensor = far_right_light_sensor


        self.one_eighty_degree_turn_range = [1000, 1500]  # time in ms for robot to turn 180 degrees
        self.ninety_degree_turn_range = [500, 700]  # time in ms for robot to turn 90 degrees

        self.has_box = False
        self.at_junction = False
        self.magnetometer_readings = []
    
    def Drive(self, direction, speed):
        self.left_motor.on(dir=direction, speed=speed)
        self.right_motor.on(dir=direction, speed=speed)

    def Line_Sensor_readings(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        far_left_line = self.far_left_light_sensor.value()
        far_right_line = self.far_right_light_sensor.value()
        return left_line, right_line, far_left_line, far_right_line
    
    def Line_following(self):
        left_line, right_line, _, _ = self.Line_Sensor_readings()
        if left_line == 0 and right_line == 1:
            #print("Adjusting. Turning right.")
            self.right_motor.speed -= 25
        if left_line == 1 and right_line == 0:
            #print("Adjusting. Turning left.")
            self.left_motor.speed -= 25
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
        
    def is_at_junction(self):
        left_line, right_line, far_left_line, far_right_line = self.Line_Sensor_readings()
        if far_left_line == 1 or far_right_line == 1 or (left_line == 0 and right_line == 0):
            self.at_junction = True
            return True
        return False
    
    def turn(self, LorR):
        # LorR (Left or Right) is -1 for left and 1 for right.
        self.turning_sequence(LorR)
    
    def Forward_Until_Node(self, speed):
        while self.is_at_junction() == False:
            self.Drive(1, speed)
            self.Line_following()
            sleep_ms(20)
        sleep_ms(150)
        self.reset()
        
    def turning_sequence(self, LorR):
        # LorR (Left or Right) is -1 for left and 1 for right.
        # time for robot's wheels to reach the line before turning
        # needs to be tested and adjusted for speed of robot
        self.Drive(1, 100)
        sleep_ms(400)
        if LorR == -1:
            print("Executing left turn (tank drive)")
            self.right_motor.on(dir=1, speed=100)
            self.left_motor.on(dir=0, speed=100)
        if LorR == 1:
            print("Executing right turn (tank drive)")
            self.left_motor.on(dir=1, speed=100)
            self.right_motor.on(dir=0, speed=100)
        # Turns for a set time or until line is detected again. 
        # rot_range is set primarily to allow ensure the robot as approximately turned sufficiently
        # (i.e. in case it detects a line somewhere before turning 90).
        # It also acts as a safety in case the robot misses the line, to prevent it from continuing to turn indefinitely
        line_detection(self.ninety_degree_turn_range, self.left_light_sensor, self.right_light_sensor)

    def one_eighty_degree_turn(self):
        print("Executing 180 degree turn (tank drive)")
        self.left_motor.on(dir=1, speed=80)
        self.right_motor.on(dir=0, speed=80)
        # Buffer time for line detection to ensure the robot doesn't immediately detect the line before turning 180 degrees. 
        # Needs to be tested and adjusted for speed of robot
        sleep_ms(100)
        line_detection(self.one_eighty_degree_turn_range, self.left_light_sensor, self.right_light_sensor)

    def reverse_turn(self, turn):
        _, _, far_left_line, far_right_line = self.Line_Sensor_readings()
        # Reverses till junction
        while far_left_line == 1 or far_right_line == 1:
            # Reverse
            self.Drive(0, 100)
            _, _, far_left_line, far_right_line = self.Line_Sensor_readings()
            self.Line_following()
            sleep_ms(20)
        while far_left_line == far_right_line == 0:
            # Reverse
            self.Drive(0, 100)
            _, _, far_left_line, far_right_line = self.Line_Sensor_readings()
            self.Line_following()
            sleep_ms(20)
        # Carries out turn in the same manner as driving forwards.
        self.Drive(1, 100)
        sleep_ms(50)
        self.turning_sequence(turn)

    def motion_control(self):
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        print("turning")
        check = self.turn(-1)
        '''
        if not check:
            self.find_line()
        '''
        print("turning complete")
        self.Forward_Until_Node(100)
        print("turning")
        check = self.turn(-1)
        print("turning complete")
        self.Forward_Until_Node(100)
        self.reverse_turn(1)
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        print("turning")
        check = self.turn(-1)
        print("turning complete")
        self.Forward_Until_Node(100)
        self.reverse_turn(-1)
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        print("turning")
        check = self.turn(1)
        print("turning complete")
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)






    
    def update(self):
        #self.motion_control()
        # Control frequency of robot update loop to prevent overloading the CPU (set to 50 Hz)
        self.motion_control()
        return False
    
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
        return True
    
    def test_servos(self):
        print("Move to 0°")
        self.forklift_servo.set_angle(0)
        self.claw_servo.set_angle(0)
        sleep_ms(2000)

        print("Move to 135° (centre)")
        self.forklift_servo.set_angle(135)
        self.claw_servo.set_angle(135)
        sleep_ms(2000)

        print("Move to 270°")
        self.forklift_servo.set_angle(270)
        self.claw_servo.set_angle(270)
        sleep_ms(2000)
        return True
    
    def test_light_sensors(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        far_left_line = self.far_left_light_sensor.value()
        far_right_line = self.far_right_light_sensor.value()
        print(f"left_light_sensor: {left_line}, right_light_sensor: {right_line}, far_left_light_sensor: {far_left_line}, far_right_light_sensor: {far_right_line}")
        sleep_ms(100)
        return True
        
    def test_180(self):
        left_line, right_line, _, _ = self.Line_Sensor_readings()
        if left_line == right_line == 0:
            self.one_eighty_degree_turn()
        else:
            self.Drive(1, 100)
            self.Line_following()
            sleep_ms(20)
            
    def test_magnetometer(self):
        if self.magnetometer is not None:
            self.magnetometer.plot()
            return True
        else:
            print("Magnetometer not initialized.")
            return False
        
        
        
        
