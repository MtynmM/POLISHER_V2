from gpiozero import PWMOutputDevice

class LissaModel:
    def __init__(self, pin_number):
        """Lissa spins at duty cycle 0.5 speed"""
        self.pin = pin_number
        self.FIXED_SPEED = 0.5
        self.motor = PWMOutputDevice(self.pin, frequency=1000)

    def set_state(self, is_on: bool):
        if is_on:
            self.motor.value = self.FIXED_SPEED
        else:
            self.motor.value = 0

    def close(self):
        self.motor.close()

