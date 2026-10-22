from machine import Pin, Timer
from utime import sleep


class LED:
    def __init__(self, pin):
        self.led = Pin(pin, Pin.OUT)
        self.timer = Timer(-1)

    def start_flash(self):
        self.timer.init(period=500, mode=Timer.PERIODIC, callback=self.toggle)

    def stop_flash(self):
        self.timer.deinit()
        self.led.off()

    def toggle(self, timer):
        self.led.toggle()

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

        


