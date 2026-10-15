from utime import ticks_ms, sleep_ms

def line_detection(rot_time, left_light_sensor, right_light_sensor):
    t0 = ticks_ms()
    while ticks_ms() - t0 < rot_time:
        left_line = left_light_sensor.value()
        right_line = right_light_sensor.value()
        if left_line == 1 and right_line == 1:
            print("Line detected. Stopping turn.")
        break