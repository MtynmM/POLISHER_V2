from gpiozero import PWMOutputDevice

class LightModel:
    def __init__(self, pin_number):
        self.pin=pin_number
        self.current_brightness = 0 
        self.led=PWMOutputDevice(self.pin,frequency=1000)

    def set_brightness(self, brightness):
        """set brightness from 0 to 100 and convert to duty cycle"""
        if brightness < 0 : brightness = 0
        if brightness > 100 : brightness = 100
        self.current_brightness = brightness
        self.led.value = float(brightness / 100.0)

    def close(self):
        """Cleanup the hardware resources"""
        self.led.close()