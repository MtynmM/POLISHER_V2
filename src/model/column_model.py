from gpiozero import DigitalOutputDevice

class ColumnModel:
    def __init__(self, en_pin, dir_pin):
        """
        مدل کنترل بازوی آسانسوری (تمام دیجیتال)
        :param en_pin: پین فعال‌ساز (Enable/Pulse) - فقط روشن/خاموش
        :param dir_pin: پین جهت (Direction)
        """
        self.en_pin = en_pin
        self.dir_pin = dir_pin

        # تعریف درایورها به صورت دیجیتال (بدون PWM)
        self.motor_enable = DigitalOutputDevice(self.en_pin)
        self.motor_dir = DigitalOutputDevice(self.dir_pin)
        
        print(f" Column Motor initialized (DIGITAL): EN={en_pin}, DIR={dir_pin}")

    def move_up(self):
        """حرکت به بالا"""
        self.motor_dir.on()      # جهت بالا (مثلاً ۱)
        self.motor_enable.on()   # روشن کردن موتور (سرعت ثابت)

    def move_down(self):
        """حرکت به پایین"""
        self.motor_dir.off()     # جهت پایین (مثلاً ۰)
        self.motor_enable.on()   # روشن کردن موتور

    def stop(self):
        """توقف کامل"""
        self.motor_enable.off()  # خاموش کردن

    def close(self):
        self.motor_enable.close()
        self.motor_dir.close()