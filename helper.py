from utime import ticks_ms, sleep_ms

def line_detection(rot_range, left_light_sensor, right_light_sensor):
    t0 = ticks_ms()
    while ticks_ms() - t0 < rot_range[1]:
        left_line = left_light_sensor.value()
        right_line = right_light_sensor.value()
        if (left_line == 1 and right_line == 1) and rot_range[0] < (ticks_ms() - t0) < rot_range[1]:
            print(ticks_ms() - t0)
            print("Line detected. Stopping turn.")
            return True
    print("Line not detected. Stopping turn.")
    return False

