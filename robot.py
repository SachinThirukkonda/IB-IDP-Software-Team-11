from utime import sleep_ms, ticks_ms
from helper import line_detection
from Navigation import Navigator



class Robot:
    def __init__(self, parameters, left_motor, right_motor, forklift_servo, claw_servo, 
                 left_light_sensor, right_light_sensor, far_left_light_sensor, far_right_light_sensor, magnetometer):

        #Initialise hyperparameters
        self._init_parameters(parameters)
        
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.forklift_servo = forklift_servo
        self.claw_servo = claw_servo

        self.magnetometer = magnetometer

        self.left_light_sensor = left_light_sensor
        self.right_light_sensor = right_light_sensor
        
        self.far_left_light_sensor = far_left_light_sensor
        self.far_right_light_sensor = far_right_light_sensor

        self.side = None

        self.current_node = None

    '''
    Helper Methods
    '''
    def drive(self, direction, speed):
        self.left_motor.on(dir=direction, speed=speed)
        self.right_motor.on(dir=direction, speed=speed)

    def line_Sensor_readings(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        far_left_line = self.far_left_light_sensor.value()
        far_right_line = self.far_right_light_sensor.value()
        return left_line, right_line, far_left_line, far_right_line
    
    def line_following(self):
        left_line, right_line, _, _ = self.line_Sensor_readings()
        if left_line == 0 and right_line == 1:
            #print("Adjusting. Turning right.")
            self.right_motor.speed -= self.motor_correction
        if left_line == 1 and right_line == 0:
            #print("Adjusting. Turning left.")
            self.left_motor.speed -= self.motor_correction
        self.left_motor.update()
        self.right_motor.update()
        
    def is_at_junction(self):
        left_line, right_line, far_left_line, far_right_line = self.line_Sensor_readings()
        if far_left_line == 1 or far_right_line == 1 or (left_line == 0 and right_line == 0):
            self.at_junction = True
            return True
        return False
    
    def turning_sequence(self, LorR):
        # LorR (Left or Right) is -1 for left and 1 for right.
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

    def move_to_box(self, speed):
        while self.magnetometer.value() == 0:
            self.magnetometer.update()
            self.drive(1, speed)
            self.line_following()
            sleep_ms(self.control_period)
            polarity = self.magnetometer.value()
        return polarity
            
    def update_side(self, side):
        self.side = side

    def reset(self):
        self.left_motor.off()
        self.right_motor.off()
        self.claw_servo.reset()
        self.forklift_servo.reset()

    '''
    Motion Methods
    '''

    def Forward_Until_Node(self, speed):
        while self.is_at_junction() == False:
            self.drive(1, speed)
            self.line_following()
            sleep_ms(self.control_period)
        self.reset()

    def Turn(self, LorR):
        # LorR (Left or Right) is -1 for left and 1 for right.
        # time for robot's wheels to reach the line before turning
        # needs to be tested and adjusted for speed of robot
        self.drive(1, 100)
        sleep_ms(self.turning_sleep_time)
        self.turning_sequence(LorR)

    def Reverse_Turn(self, turn):
        _, _, far_left_line, far_right_line = self.line_Sensor_readings()

        # Reverses till junction
        while far_left_line == 1 or far_right_line == 1:
            # Reverse
            self.drive(0, 100)
            self.line_following()         
            sleep_ms(self.control_period)
            _, _, far_left_line, far_right_line = self.line_Sensor_readings()   
        
        while far_left_line == far_right_line == 0:
            # Reverse
            self.drive(0, 100)
            self.line_following()
            sleep_ms(self.control_period)
            _, _, far_left_line, far_right_line = self.line_Sensor_readings()
        
        # Carries out turn in the same manner as driving forwards.
        self.drive(1, 100)
        sleep_ms(self.reverse_turning_sleep_time)
        self.turning_sequence(turn)

    def One_Eighty_Degree_Turn(self):
        print("Executing 180 degree turn (tank drive)")
        self.left_motor.on(dir=1, speed=80)
        self.right_motor.on(dir=0, speed=80)
        line_detection(self.one_eighty_degree_turn_range, self.left_light_sensor, self.right_light_sensor)

    '''
    Box Collection and Drop-off Methods
    '''

    def Collect_Box(self):
        # Reset robot to ensure it is not moving and servos are in the correct position
        self.reset()
        # Move to box until magnetometer detects it
        box_polarity = self.move_to_box(30) 

        #Close claws on box and lift it up       
        self.claw_servo.set_angle(0)
        sleep_ms(500)
        self.forklift_servo.set_angle(0)
        
        return box_polarity

    def Drop_Box(self):
        self.forklift_servo.reset()
        sleep_ms(500)
        self.claw_servo.reset()
    
    def motion_control_test(self):
        self.Forward_Until_Node(100)
        print("turning")
        check = self.Turn(1)
        print("turning complete")
        self.Forward_Until_Node(100)
        print("turning")
        check = self.Turn(1)
        print("turning complete")
        self.Forward_Until_Node(100)
        self.Forward_Until_Node(100)
        self.Reverse_Turn(-1)
        self.Turn(1)
        
    def update(self):
        self.motion_control_test()
        # Control frequency of robot update loop to prevent overloading the CPU (set to 50 Hz)
        sleep_ms(self.control_period)
        return False
    


    def _init_parameters(self, parameters):
        # Default values for hyperparameters, will need to change later.
        self.one_eighty_degree_turn_range = [1000, 1500]  # time in ms for robot to turn 180 degrees
        self.ninety_degree_turn_range = [500, 700]  # time in ms for robot to turn 90 degrees
        self.motor_correction = 25  # Amount to adjust motor speed for line following
        self.turning_sleep_time = 500  # Sleep time during turning actions
        self.reverse_turning_sleep_time = 550  # Sleep time during reverse turning actions
        self.control_frequency = 50  # Control frequency in Hz
        self.control_period = 1000 // self.control_frequency  # Control period in ms

        # Change any default values to custom values for specified hyperparameters
        for param, val in parameters.items():
            exec('self.' + param + ' = ' + str(val))

    '''
    Test Functions
    '''

    def test_motors(self):
        print("Forward")
        self.left_motor.on(dir=1, speed=100)
        self.right_motor.on(dir=1, speed=100)

        sleep_ms(1000)
        print("Reverse")
        self.left_motor.on(dir=0, speed=100)
        self.right_motor.on(dir=0, speed=100)
        sleep_ms(1000)
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
        left_line, right_line, _, _ = self.line_Sensor_readings()
        if left_line == right_line == 0:
            self.One_Eighty_Degree_Turn()
        else:
            self.drive(1, 100)
            self.line_following()
            sleep_ms(20)
                    
    def test_magnetometer(self):        
        if self.magnetometer is not None:           
            self.magnetometer.plot()           
            self.magnetometer.test()           
            return True      
        else:            
            print("Magnetometer not initialized.")    
            return False
        
        
