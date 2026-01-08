import logging

# تنظیمات پین‌ها (مدیر پروژه باید این پین‌ها را پروب کند)
PIN_CONFIG = {
    "PAD_PWM": 18,       # پین PWM برای سرعت موتور پد (Physical Pin 12)
    "LIGHT_PWM": 13,     # پین PWM برای شدت نور (Physical Pin 33)
    "COLUMN_DIR": 23,    # پین دیجیتال برای جهت یا فعال‌سازی ستون
    "COLUMN_PULSE": 24   # پین پالس برای استپر (برای نمایش حرکت)
}

class HardwareBridge:
    """
    این کلاس مستقیماً با GPIOهای رزبری‌پای صحبت می‌کند.
    اگر کتابخانه gpiozero نصب نباشد (روی ویندوز)، حالت شبیه‌سازی فعال می‌شود.
    """
    def __init__(self):
        self.mock_mode = False
        self.pad_device = None
        self.light_device = None
        self.col_enable = None
        
        try:
            from gpiozero import PWMOutputDevice, DigitalOutputDevice
            # راه‌اندازی دستگاه‌های واقعی
            self.pad_device = PWMOutputDevice(PIN_CONFIG["PAD_PWM"], frequency=1000)
            self.light_device = PWMOutputDevice(PIN_CONFIG["LIGHT_PWM"], frequency=1000)
            self.col_enable = DigitalOutputDevice(PIN_CONFIG["COLUMN_DIR"])
            print(f"✅ RASPBERRY PI GPIO DETECTED. Active Pins: {PIN_CONFIG}")
            
        except ImportError:
            self.mock_mode = True
            print("⚠️ GPIO NOT DETECTED. Running in MOCK MODE (Simulation Only).")
        except Exception as e:
            print(f"❌ GPIO ERROR: {e}")
            self.mock_mode = True

    def update_hardware(self, state):
        """
        این متد وضعیت (State) را از برنامه می‌گیرد و روی پین‌ها اعمال می‌کند.
        """
        if self.mock_mode:
            return

        try:
            # 1. کنترل موتور پد (PWM)
            # مقدار ورودی 0 تا 100 است، باید به 0.0 تا 1.0 تبدیل شود
            pad_val = state.get("pad_speed", 0) / 100.0
            if self.pad_device.value != pad_val: # فقط اگر تغییر کرده اعمال کن
                self.pad_device.value = pad_val

            # 2. کنترل نور (PWM)
            light_val = state.get("light_intensity", 0) / 100.0
            if self.light_device.value != light_val:
                self.light_device.value = light_val

            # 3. کنترل ستون (Digital)
            # وقتی is_moving فعال است، پین را روشن می‌کنیم (3.3V)
            is_moving = state.get("is_moving", False)
            if is_moving:
                self.col_enable.on()
            else:
                self.col_enable.off()

        except Exception as e:
            print(f"HW Write Error: {e}")

    def cleanup(self):
        if not self.mock_mode:
            if self.pad_device: self.pad_device.close()
            if self.light_device: self.light_device.close()
            if self.col_enable: self.col_enable.close()
            print("GPIO Cleaned up.")