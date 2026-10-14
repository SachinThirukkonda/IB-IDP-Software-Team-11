from utime import sleep_ms
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

        self.running = False
    
    def Drive_forward(self, speed):
        self.left_motor.Forward(speed)
        self.right_motor.Forward(speed)
    
    def Line_following(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        if left_line == 0 and right_line == 1:
            print("Adjusting. Turning right.")
            self.right_motor.speed -= 20
        if left_line == 1 and right_line == 0:
            print("Adjusting. Turning left.")
            self.left_motor.speed -= 20
        self.left_motor.update()
        self.right_motor.update()
    
    def check_for_bend(self):
        sleep_ms(200)
        # Execute 90 degree turn if white detected on far sensors
        left_line = self.far_left_light_sensor.value()
        right_line = self.far_right_light_sensor.value()

        if left_line == 0 and right_line == 1:
            print("Executing right turn (tank drive)")
            self.left_motor.Forward(speed = 100)
            self.right_motor.Reverse(speed = 100)
            sleep_ms(1200)

        if left_line == 1 and right_line == 0:
            print("Executing left turn (tank drive)")
            self.right_motor.Forward(speed = 100)
            self.left_motor.Reverse(speed = 100)
            sleep_ms(1200)

        if left_line == 1 and right_line == 1:
            # Update for later for case where line splits in 2
            pass
    
    def update(self):
        self.Drive_forward(100)
        self.Line_following()
        print(f"left_motor: {self.left_motor.speed}   right_motor: {self.right_motor.speed}")
        sleep_ms(100)
    
    def reset(self):
        self.left_motor.off()
        self.right_motor.off()
    
    def test_motors(self):
        print("Forward")
        self.left_motor.Forward(speed = 100)
        self.right_motor.Forward(speed = 100)
        
        sleep_ms(10)
        print("Reverse")
        self.left_motor.Reverse(speed = 100)
        self.right_motor.Reverse(speed = 100)
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
        

        
        
        
        
