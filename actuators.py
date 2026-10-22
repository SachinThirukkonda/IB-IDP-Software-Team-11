from machine import Pin, PWM

class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        self.speed = 0
        
    def off(self):
        self.pwm.duty_u16(0)
        
    def on(self, dir=1, speed=None):
        if speed != None:
            self.speed = speed
        self.mDir.value(dir)                  # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * self.speed / 100))  # speed range 0-100 motor
        
    def update(self):
        self.pwm.duty_u16(int(65535 * self.speed / 100))
        
class Servo:
    # Common settings for 270° servos:
    # 0.5 ms → minimum (0°)
    # 2.5 ms → maximum (270°)
    # Total span = 2.0 ms
    # Frequency: 50 Hz (20 ms period)
    # 
    # Duty % = Pulse width / Period x 100
    # Minimum (0°) = 0.5/20
    # Centre (135°) = 1.5/20
    # Maximum (270°) = 2.5/20
    #
    # Convert to Pico PWM (16-bit)
    # Pico uses: 0 → 65535
    # Duty value = Duty Fraction x 65535
    # Minimum (0.5 ms) = 0.025 * 65535
    # Centre (1.5 ms) = 0.075 * 65535
    # Maximum (2.5 ms) = 0.0125 * 65535
    MIN_DUTY = 1638 # 0°
    MID_DUTY = 4915 # 135°
    MAX_DUTY = 8192 # 270°
    
    def __init__(self, ServoPin, init_angle):
        self.servo = PWM(ServoPin)
        self.servo.freq(50)  # 50 Hz for servo
        self.reset_angle = init_angle
        self.set_angle(init_angle)
 
    # Convert angle (0–270) to duty
    def set_angle(self, angle):
       # Clamp angle
       if angle < 0:
           angle = 0
       if angle > 270:
           angle = 270
 
       duty = int(Servo.MIN_DUTY + (angle / 270) * (Servo.MAX_DUTY - Servo.MIN_DUTY))
       self.servo.duty_u16(duty)


    def reset(self):
        self.set_angle(self.reset_angle)
        
    