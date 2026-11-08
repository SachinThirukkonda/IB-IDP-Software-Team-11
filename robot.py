from utime import sleep_ms, ticks_ms

class Robot:
    def __init__(self, parameters, left_motor, right_motor, forklift_servo, claw_servo, 
                 left_light_sensor, right_light_sensor, far_left_light_sensor, far_right_light_sensor, magnetometer,
                 collection_distance_sensor, dropoff_distance_sensor,
                 led_green, led_red, led_yellow):
            
        #Initialise hyperparameters
        self._init_parameters(parameters)
        
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.forklift_servo = forklift_servo
        self.claw_servo = claw_servo
        self.forklift_servo.set_angle(self.forklift_default_angle)
        self.claw_servo.set_angle(self.claw_open_angle)

        self.magnetometer = magnetometer

        self.collection_distance_sensor = collection_distance_sensor
        self.dropoff_distance_sensor = dropoff_distance_sensor

        self.left_light_sensor = left_light_sensor
        self.right_light_sensor = right_light_sensor
        self.far_left_light_sensor = far_left_light_sensor
        self.far_right_light_sensor = far_right_light_sensor

        self.led_green = led_green
        self.led_red = led_red
        self.led_yellow = led_yellow

        self.at_junction = False
        self.has_box = False
        self.box_polarity = 0
        self.box_detected = False


    '''
    Helper Methods
    '''
    def drive(self, direction, speed):
        self.left_motor.on(dir=direction, speed=speed)
        self.right_motor.on(dir=direction, speed=speed)

    def _set_box_polarity_leds(self, polarity):
        # Show the carried box pole with one steady LED.
        if self.led_red:
            self.led_red.off()
        if self.led_green:
            self.led_green.off()

        if polarity == 1 and self.led_red:  # North pole
            self.led_red.on()
        elif polarity == -1 and self.led_green:  # South pole
            self.led_green.on()

    def line_Sensor_readings(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        far_left_line = self.far_left_light_sensor.value()
        far_right_line = self.far_right_light_sensor.value()
        return left_line, right_line, far_left_line, far_right_line
    
    def line_following(self, direction, speed):
        correction_factor = speed / 100  # Adjust correction based on speed
        left_line, right_line, far_left_line, far_right_line = self.line_Sensor_readings()
        # Adjust motor speeds based on line sensor readings
        if left_line == 0 and right_line == 1 and direction == 1:
            self.right_motor.speed *= (100-self.motor_correction*correction_factor)/100
        if left_line == 1 and right_line == 0 and direction == 1:
            self.left_motor.speed *= (100-self.motor_correction*correction_factor)/100
        if left_line == 0 and right_line == 1 and direction == 0:
            self.right_motor.speed *= (100-self.motor_correction*correction_factor)/100
        if left_line == 1 and right_line == 0 and direction == 0:
            self.left_motor.speed *= (100-self.motor_correction*correction_factor)/100

        # Adjust motor speeds based on far line sensor readings. If the the far sensor detects a line, a greater correction is needed to correct the robot's path.
        if far_left_line == 0 and far_right_line == 1 and left_line == right_line == 0 and direction == 1:
            self.right_motor.speed *= 2 * (100-self.motor_correction*correction_factor)/100
        if far_left_line == 1 and far_right_line == 0 and left_line == right_line == 0 and direction == 1:
            self.left_motor.speed *= 2 * (100-self.motor_correction*correction_factor)/100
        if far_left_line == 0 and far_right_line == 1 and left_line == right_line == 0 and direction == 0:
            self.right_motor.speed *= 2 * (100-self.motor_correction*correction_factor)/100
        if far_left_line == 1 and far_right_line == 0 and left_line == right_line == 0 and direction == 0:
            self.left_motor.speed *= 2 * (100-self.motor_correction*correction_factor)/100
        self.left_motor.update()
        self.right_motor.update()

    def line_detection(self, rot_range):
        t0 = ticks_ms()
        while ticks_ms() - t0 < rot_range[1]:
            # Check if line is detected by either left or right light sensor within the specified rotation range before stopping the turn.
            if (self.right_light_sensor.value() == 1 or self.left_light_sensor.value() == 1) and rot_range[0] < (ticks_ms() - t0) < rot_range[1]:
                print("Line detected. Stopping turn.")
                return True
        print("Line not detected. Stopping turn.")
        return False
    
    def is_at_junction(self):
        # Check if the robot is at a junction by checking the readings of all line sensors. If any of the far sensors detect a line, or if all sensors detect no line, it is considered to be at a junction.
        left_line, right_line, far_left_line, far_right_line = self.line_Sensor_readings()
        if far_left_line == 1 or far_right_line == 1 or (left_line == right_line == far_left_line == far_right_line == 0):
            self.at_junction = True
            return True
        return False
    
    def turning_sequence(self, LorR):
        # LorR (Left or Right) is -1 for left and 1 for right.
        if LorR == -1:
            print("Executing left turn (tank drive)")
            self.right_motor.on(dir=1, speed=self.turning_speed)
            self.left_motor.on(dir=0, speed=self.turning_speed)
        if LorR == 1:
            print("Executing right turn (tank drive)")
            self.left_motor.on(dir=1, speed=self.turning_speed)
            self.right_motor.on(dir=0, speed=self.turning_speed)
        # Turns for a set time or until line is detected again. 
        # rot_range is set primarily to allow ensure the robot as approximately turned sufficiently
        # (i.e. in case it detects a line somewhere before turning 90).
        # It also acts as a safety in case the robot misses the line, to prevent it from continuing to turn indefinitely
        self.line_detection(self.ninety_degree_turn_range)
        sleep_ms(50)

    def move_to_box(self, speed):
        t0 = ticks_ms()
        # Move forward until the collection distance sensor detects a box or until the collection time expires.
        while self.collection_distance_sensor.value() > 60 and ticks_ms() < (t0 + self.collection_time):
            self.drive(1, speed)
            self.line_following(1, speed)
            self.collection_distance_sensor.test()
            sleep_ms(self.control_period)
        if ticks_ms() >= (t0 + self.collection_time):
            # Aborted
            sleep_ms(self.collection_time)
            print("Box not found")
            return 0
        else:
            print("Box found")
            return 1
        
    def find_box_polarity(self):
        t0 = ticks_ms()
        polarity = 0
        tick = 0
        self.magnetometer.update()
        # Check the magnetometer for a short period of time to determine the polarity of the box.
        while self.magnetometer.value() == 0 and ticks_ms() < (t0 + 500):
            self.magnetometer.update()
            tick += 1
            sleep_ms(self.control_period)
            polarity = self.magnetometer.value()
            print(f"Polarity: {polarity}")
        polarity = self.magnetometer.value()
        self.box_polarity = polarity
        self.has_box = self.box_polarity in (-1, 1)
        if self.has_box:
            return polarity
        #  If no polarity is detected, return 1 or -1 based on the tick count. 
        # This produces a pseudo-random result and ensures that the robot can still drop the box if the magnetometer fails to detect a polarity.
        tick %= 2
        if tick == 0:
            return 1
        else:
            return -1
    
    def reset(self):
        self.left_motor.off()
        self.right_motor.off()
        self.claw_servo.set_angle(self.claw_open_angle)
        self.forklift_servo.set_angle(self.forklift_default_angle)

    '''
    Motion Methods
    '''

    def Forward_Until_Node(self, speed, check=True):
        self.drive(1, speed)
        # Move forward until the robot is no longer at a junction, then continue moving forward until it reaches the next junction.
        while self.is_at_junction() == True:
            self.drive(1, speed)
            self.line_following(1, speed)

            sleep_ms(self.control_period)
        while self.is_at_junction() == False:
            self.drive(1, speed)
            self.line_following(1, speed)
            left_line, right_line, far_left_line, far_right_line = self.line_Sensor_readings()
            if check == True and left_line == right_line == far_left_line == far_right_line == 0:
                print("Derailed from line. Stopping.")
                self.drive(1, 0)
                raise RuntimeError("Robot lost the line while moving to the next node")
                
            sleep_ms(self.control_period)
        
        self.drive(1, 0)



    def Forward_Until_Rack(self, speed, time=2000):
        """Follow the line toward a rack until it is detected or time expires."""
        t0 = ticks_ms()
        self.box_detected = False
        self.drive(1, speed)

        # Move forward until the dropoff distance sensor detects a box or time expires.
        # If a box is detected, then the program returns that a box was detected, which is used in later algorithms.
        while time is None or ticks_ms() - t0 < time:
            if self.dropoff_distance_sensor is None:
                print("Dropoff distance sensor is not configured.")
            else:
                distance = self.dropoff_distance_sensor.value()
                print(f"Dropoff distance: {distance}")
                if distance <= 150:
                    self.box_detected = True
                    break

            self.drive(1, speed)
            self.line_following(1, speed)
            sleep_ms(self.control_period)

        self.drive(1, 0)

        #If a box is not detected, the program proceeds to drop the box off.
        if not self.box_detected:
            self.Forward_Until_Node(speed=50, check=False)  # Move forward a bit to ensure the box is in position
        return self.box_detected


    def Turn(self, LorR):
        # LorR (Left or Right) is -1 for left and 1 for right.
        # time for robot's wheels to reach the line before turning
        # needs to be tested and adjusted for speed of robot
        self.drive(1, self.turning_speed)
        sleep_ms(self.turning_sleep_time)
        self.turning_sequence(LorR)

    def Reverse_Turn(self, turn):
        _, _, far_left_line, far_right_line = self.line_Sensor_readings()
        t0 = ticks_ms()
        #  Reverses for a set time to return to the junction. This is because the robot over shoots when collecting the box.
        while ticks_ms() - t0 < 1000:
            self.drive(0, self.speed)
            sleep_ms(self.control_period)
        # Reverses until the robot is no longer at a junction, then continues reversing until it reaches the next junction.
        while far_left_line == 1 or far_right_line == 1:
            # Reverse
            self.drive(0, self.speed)
            self.line_following(0, 60)
            sleep_ms(self.control_period)
            print("Reversing to junction1")
            _, _, far_left_line, far_right_line = self.line_Sensor_readings()   
        
        while far_left_line == far_right_line == 0:
            # Reverse
            self.drive(0, self.speed)
            self.line_following(0, 60)
            sleep_ms(self.control_period)
            print("Reversing to junction2")
            _, _, far_left_line, far_right_line = self.line_Sensor_readings()
        
        # Carries out turn in the same manner as driving forwards.
        self.drive(1, 0)
        # Sleep to allow the robot to stop before turning. This is to prevent the robot from jerking when suddenly changing speed.
        sleep_ms(100)
        self.drive(1, self.speed)
        sleep_ms(self.reverse_turning_sleep_time)
        self.turning_sequence(turn)

    def One_Eighty_Degree_Turn(self):
        print("Executing 180 degree turn (tank drive)")
        self.left_motor.on(dir=1, speed=self.turning_speed)
        self.right_motor.on(dir=0, speed=self.turning_speed)
        self.line_detection(self.one_eighty_degree_turn_range)

    '''
    Box Collection and Drop-off Methods
    '''

    def Collect_Box(self):
        # Reset robot to ensure it is not moving and servos are in the correct position
        self.reset()
        sleep_ms(1000)
        # Move to box until magnetometer detects it
        self.has_box = self.move_to_box(50) 
        self.drive(1, 0)
        
        if self.has_box:
            #Close claws on box and lift it up  
            self.forklift_servo.set_angle(self.forklift_lower_angle)    
            sleep_ms(1000) 
            self.claw_servo.set_angle(self.claw_close_angle)
            sleep_ms(1000)
        self.forklift_servo.set_angle(self.forklift_default_angle)
        box_polarity = self.find_box_polarity()
        print(f"Box polarity: {box_polarity}")

        self._set_box_polarity_leds(box_polarity)
        
        return box_polarity

    def Drop_Box(self):
        # Drive forwards till rack
        sleep_ms(0)

        # Stop
        self.drive(1, 0)

        self.forklift_servo.set_angle(self.forklift_raise_angle)
        sleep_ms(1000)
        self.claw_servo.set_angle(self.claw_open_angle)
        sleep_ms(1000)
        self.has_box = False
        self.box_polarity = 0
        self._set_box_polarity_leds(0)
        # Reset robot to ensure it is not moving and servos are in the correct position
        self.reset()

    def _init_parameters(self, parameters):
        # Default values for hyperparameters, will need to change later.
        self.one_eighty_degree_turn_range = [1000, 1500]  # time in ms for robot to turn 180 degrees
        self.ninety_degree_turn_range = [500, 700]  # time in ms for robot to turn 90 degrees
        self.motor_correction = 25  # Amount to adjust motor speed for line following
        self.turning_sleep_time = 500  # Sleep time during turning actions
        self.reverse_turning_sleep_time = 550  # Sleep time during reverse turning actions
        self.control_frequency = 50  # Control frequency in Hz
        self.control_period = 1000 // self.control_frequency  # Control period in ms
        self.claw_close_angle = 0
        self.forklift_default_angle = 0
        self.claw_open_angle = 20
        self.forklift_lower_angle = 120
        self.forklift_raise_angle = 180
        self.collection_time = 1000
        self.left_motor_bias = 0  # Amount to adjust left motor speed for line following
        self.right_motor_bias = 0  # Amount to adjust right motor speed for line following
        self.speed = 100
        self.turning_speed = 100

        # Change any default values to custom values for specified hyperparameters
        for param, val in parameters.items():
            setattr(self, param, val)

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

    def open_close(self):
        self.claw_servo.set_angle(self.claw_open_angle)
        print("open")
        sleep_ms(1000)
        self.claw_servo.set_angle(self.claw_close_angle)
        print("close")
        sleep_ms(1000)
        return True

    def up_down(self):
        self.forklift_servo.set_angle(self.forklift_default_angle)
        print("default")
        sleep_ms(3000)
        self.forklift_servo.set_angle(self.forklift_lower_angle)
        print("lower")
        sleep_ms(1000)
        self.forklift_servo.set_angle(self.forklift_default_angle)
        print("default")
        sleep_ms(1000)
        self.forklift_servo.set_angle(self.forklift_raise_angle)
        print("raise")
        sleep_ms(3000)
        return True

    def test_claw_and_forklift(self):
        self.claw_servo.set_angle(self.claw_open_angle)
        print("open: empty, box dropped off")
        sleep_ms(1000)
        self.forklift_servo.set_angle(self.forklift_default_angle)
        print("default: moving to box")
        sleep_ms(5000)
        self.forklift_servo.set_angle(self.forklift_lower_angle)
        print("lower")
        sleep_ms(1000)
        self.claw_servo.set_angle(self.claw_close_angle)
        print("close: box acquired")
        sleep_ms(1000)
        self.forklift_servo.set_angle(self.forklift_default_angle)
        print("default: moving to rack")
        sleep_ms(5000)
        self.forklift_servo.set_angle(self.forklift_raise_angle)
        print("raise")
        sleep_ms(3000)
        return True

    def test_box_collection(self):
        self.Collect_Box()
        sleep_ms(5000)
        self.Drop_Box()

    def test_light_sensors(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        far_left_line = self.far_left_light_sensor.value()
        far_right_line = self.far_right_light_sensor.value()
        print(f"left_light_sensor: {left_line}, right_light_sensor: {right_line}, far_left_light_sensor: {far_left_line}, far_right_light_sensor: {far_right_line}")
        sleep_ms(100)
        return True

    def test_distance_sensors(self):
        #print(f"Collection distance sensor reading: {self.collection_distance_sensor.value()}")
        print(f"Dropoff distance sensor reading: {self.dropoff_distance_sensor.value()}")
        sleep_ms(100)
        return True
        
    def test_180(self):
        left_line, right_line, _, _ = self.line_Sensor_readings()
        if left_line == right_line == 0:
            self.One_Eighty_Degree_Turn()
        else:
            self.drive(1, 100)
            self.line_following(1, 100)
            sleep_ms(20)
                    
    def test_magnetometer(self):        
        if self.magnetometer is not None:

            self.magnetometer.update()                  
            print(self.magnetometer.value())
            sleep_ms(self.control_period)          
            return True      
        else:            
            print("Magnetometer not initialized.")    
            return False

    def test_dropoff(self):
        self.claw_servo.set_angle(self.claw_close_angle)
        sleep_ms(1000)
        box_detected = self.Forward_Until_Rack(self.speed)
        if box_detected:
            print("Box detected at rack.")
            self.Reverse_Turn(-1)
        else:
            sleep_ms(1000)
            self.Drop_Box()
            sleep_ms(1000)
        return True

    def test_dropoff_distance_sensor(self):
        self.claw_servo.set_angle(self.claw_close_angle)
        print(f"Dropoff distance sensor reading: {self.dropoff_distance_sensor.value()}")
        sleep_ms(100)
        return True
    
    def reverse_drive_test(self):
        self.drive(0, self.speed)
        self.line_following(0, self.speed)
        sleep_ms(self.control_period)
        
        
