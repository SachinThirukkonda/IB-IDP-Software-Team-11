class Robot:
    def __init__(self, left_motor, right_motor, forklift_servo, claw_servo, left_light_sensor, right_light_sensor):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.forklift_servo = forklift_servo
        self.claw_servo = claw_servo

        self.left_light_sensor = left_light_sensor
        self.right_light_sensor = right_light_sensor

        self.running = False
    
    def Drive_forward(self, speed):
        self.left_motor.Forward(speed)
        self.right_motor.Forward(speed)
    
    def Line_following(self):
        left_line = self.left_light_sensor.value()
        right_line = self.right_light_sensor.value()
        print(f"left_light_sensor: {left_line}, right_light_sensor: {right_line}")
        if left_line == 0 and right_line == 1:
            print("Adjusting. Turning right.")
            self.left_motor.speed += 5
        if left_line == 1 and right_line == 0:
            print("Adjusting. Turning left.")
            self.right_motor.speed += 5
        self.left_motor.update()
        self.right_motor.update()
            
    def update(self):
        self.Drive_forward(100)
        self.Line_following()
    
    def reset(self):
        self.left_motor.off()
        self.right_motor.off()
    
    def test_motors(self):
        print("Forward")
        self.left_motor.Forward(speed = 100)
        self.right_motor.Forward(speed = 100)
        
        sleep(10)
        print("Reverse")
        self.left_motor.Reverse(speed = 100)
        self.right_motor.Reverse(speed = 100)
        sleep(10)
    
    def test_servos(self):
       print("Move to 0°")
       self.forklift_servo.set_angle(0)
       self.claw_servo.set_angle(0)
       time.sleep(2)

       print("Move to 135° (centre)")
       self.forklift_servo.set_angle(135)
       self.claw_servo.set_angle(135)
       time.sleep(2)
 
       print("Move to 270°")
       self.forklift_servo.set_angle(270)
       self.claw_servo.set_angle(270)
       time.sleep(2)
            
        
        
        
