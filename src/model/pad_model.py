from gpiozero import PWMOutputDevice, DigitalOutputDevice

class PadModel:
    def __init__(self, pwm_pin, cw_pin, ccw_pin):
        self.pwm_pin = pwm_pin
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin
        self.current_speed = 0
        self.is_ccw = False
        self.motor = PWMOutputDevice(self.pwm_pin, frequency=1000)
        self.cw_motor = DigitalOutputDevice(self.cw_pin)
        self.ccw_motor = DigitalOutputDevice(self.ccw_pin)

    def set_speed(self, percent):
        if percent < 0: percent = 0
        if percent > 100: percent = 100
        
        self.current_speed = percent
        self.motor.value = percent / 100.0

        if percent > 0:
            self._apply_direction()
        else:
            self.stop_rotation()
        
    def set_direction(self, ccw : bool):
        self.is_ccw = ccw
        if self.current_speed > 0: self._apply_direction()

    def _apply_direction(self):
        if self.is_ccw :
            self.cw_motor.off()
            self.ccw_motor.on()
        else:
            self.cw_motor.on()
            self.ccw_motor.off()

    def stop_rotation(self):
        self.cw_motor.off()
        self.ccw_motor.off()
        self.motor.value = 0

    def close(self):
        self.motor.close()
        self.cw_motor.close()
        self.ccw_motor.close()