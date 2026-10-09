from motor import Motor

motor_left = Motor(dirPin=4, PWMPin=5)
motor_right = Motor(dirPin=6, PWMPin=7)


def adjust_motion(speed_left, speed_right, motor_left, motor_right):
    motor_left.Forward(speed = speed_left)
    motor_right.Forward(speed = speed_right)
        
adjust_motion(20,20, motor_left, motor_right)

    