from machine import Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from utime import sleep

def test_vl53l0x():
    sda = Pin(18)
    print("SDA configured")

    scl = Pin(19)
    print("SCL configured")

    i2c_bus = I2C(1, sda=sda, scl=scl, freq=100000)
    print("I2C configured")

    print("Devices found:", i2c_bus.scan())

    print([hex(address) for address in i2c_bus.scan()])
    # Setup vl53l0 object
    vl53l0 = VL53L0X(i2c_bus)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
    vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)


    while True:
        print("Starting vl53l0...")

        # Start device
        vl53l0.start()

        # Read ten samples
        for _ in range(10):
            distance = vl53l0.read()
            print(f"Distance = {distance}mm")  # Check calibration!
            sleep(0.5)
        
        # Stop device
        vl53l0.stop()

from machine import Pin, I2C

i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=100000)

print("I2C devices:", [hex(addr) for addr in i2c.scan()])

if __name__ == "__main__":
    test_vl53l0x()
