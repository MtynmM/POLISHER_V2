from gpiozero import PWMOutputDevice, DigitalOutputDevice

class ColumnModel:
    def __init__(self, pwm_pin, dir_pin):
        self.pwm_pin=pwm_pin
        self.dir_pin=dir_pin
        self.FIXED_SPEED = 0.5

        # defined speed driver(pwm)
        self.motor_speed = PWMOutputDevice(self.pwm_pin,frequency=1000)

        # defined direction driver(digital)
        self.motor_dir = DigitalOutputDevice(self.dir_pin)

        def move_up(self):
            self.motor_dir.on()
            self.motor_speed.value = self.FIXED_SPEED

        def move_down(self):
            self.motor_dir.off()
            self.motor_speed.value = self.FIXED_SPEED

        def stop(self):
            self.motor_speed.value = 0

        def close(self):
            self.motor_speed.close()
            self.motor_dir.close()
        