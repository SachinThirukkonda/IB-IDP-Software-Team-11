from machine import Pin, I2C, ADC
from libs.VL53L0X.VL53L0X import VL53L0X

class Light_Sensor:
    def __init__(self, pin):
        self.light_sensor = Pin(pin, Pin.IN, Pin.PULL_UP)
    
    def value(self):
        return self.light_sensor.value()
    
    def test(self):
        reading = self.light_sensor.value()
        print(f"Reading: {reading}")

class Magnetometer:
    def __init__(self, pin):
            self.magnetometer = ADC(pin)
        
    def value(self):
        return self.magnetometer.read_u16()
    
    def test(self):
        reading = self.magnetometer.read_u16()
        print(f"Reading: {reading}")

    def plot(self):
        reading = self.magnetometer.read_u16()
        print(f"{reading}")

class Distance_Sensor:
    def __init__(self, sda, scl):
        # config I2C Bus
        i2c_bus = I2C(0, sda=Pin(sda), scl=Pin(scl)) # I2C0 on GP8 & GP9
        # print(i2c_bus.scan())  # Get the address (nb 41=0x29, 82=0x52)

        # Setup vl53l0 object
        self.distance_sensor = VL53L0X(i2c_bus)
        self.distance_sensor.set_Vcsel_pulse_period(self.distance_sensor.vcsel_period_type[0], 18)
        self.distance_sensor.set_Vcsel_pulse_period(self.distance_sensor.vcsel_period_type[1], 14)
        
        # Start device
        self.distance_sensor.start()
    
    def value(self):
        return self.distance_sensor.read()
    
    def test(self):
        print(f"Distance: {self.distance_sensor.read()} mm")
        
    def off(self):
        # Stop device
        self.distance_sensor.stop()
        
        
        