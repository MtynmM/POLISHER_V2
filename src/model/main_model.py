import time
import threading
from threading import Lock, Event
from typing import Dict, Any

# --- لایه انتزاع سخت‌افزار (HAL) ---
IS_RASPBERRY_PI = False
#try:
#    from gpiozero import PWMOutputDevice, DigitalOutputDevice
#    IS_RASPBERRY_PI = True
#except (ImportError, OSError):
#    IS_RASPBERRY_PI = False
    # در محیط ویندوز این پیام را یکبار چاپ کن و رد شو
#    print("⚠️ [MODEL] Simulation Mode Active (No GPIO found).")

class MainModel:
    """
    Polisher V2 - Core Logic & Physics Engine (Diamond Edition)
    نسخه نهایی: دارای سیستم ترمز اضطراری و مدیریت صف حرکت.
    """

    # --- تنظیمات پین‌ها (BCM) ---
    PIN_PAD_PWM = 12
    PIN_LISSA_PWM = 13
    PIN_LIGHT_PWM = 19
    PIN_STEP_PULSE = 18
    PIN_STEP_DIR = 23

    # --- تنظیمات فیزیک استپر ---
    STEPS_PER_MM = 200        
    MIN_PULSE_DELAY = 0.0005  # سرعت نهایی (High Speed)
    MAX_PULSE_DELAY = 0.005   # سرعت شروع (Low Speed)
    RAMP_STEPS = 50           # طول باند شتاب‌گیری

    def __init__(self):
        self._hw_lock = Lock()
        
        # فلش اضطراری (Kill Switch):
        # این یک متغیر امن بین تردهاست. اگر True شود، همه موتورها باید درجا بایستند.
        self._stop_flag = Event()
        
        # نگهداری ترد فعلی حرکت ستون (برای اینکه بتوانیم چکش کنیم)
        self._motion_thread = None

        self.motors = {}
        
        # وضعیت سیستم (Single Source of Truth)
        self.state: Dict[str, Any] = {
            "pad_speed": 0,
            # [خط جدید] اضافه کردن متغیر برای حفظ سرعت تنظیمی
            "config_pad_speed": 10, 
            
            "lissa_speed": 0,
            "light_intensity": 0,
            
            # مقادیر پیش‌فرض
            "step_pad": 10,
            "step_lissa": 10,
            "step_col": 100,
            "step_light": 10,
            
            "is_moving": False,
        }

        self._init_hardware()

    def _init_hardware(self):
        global IS_RASPBERRY_PI
        if not IS_RASPBERRY_PI: return

        try:
            # موتورهای DC (کنترل سرعت)
            self.motors['pad'] = PWMOutputDevice(self.PIN_PAD_PWM, frequency=1000)
            self.motors['lissa'] = PWMOutputDevice(self.PIN_LISSA_PWM, frequency=1000)
            self.motors['light'] = PWMOutputDevice(self.PIN_LIGHT_PWM, frequency=1000)
            
            # استپر موتور (کنترل دقیق موقعیت)
            self.motors['step_dir'] = DigitalOutputDevice(self.PIN_STEP_DIR)
            self.motors['step_pulse'] = DigitalOutputDevice(self.PIN_STEP_PULSE)
            
            print("✅ [MODEL] Hardware initialized successfully.")
        except Exception as e:
            print(f"❌ [MODEL] HW Error: {e}")
            print("⚠️ [MODEL] Hardware failed. Switching to SIMULATION MODE automatically.")
            IS_RASPBERRY_PI = False

    # ==========================
    # توابع عمومی و ایمنی
    # ==========================
    
    def emergency_stop(self):
        """ترمز دستی: توقف فوری تمام موتورها"""
        print("🚨 EMERGENCY STOP TRIGGERED")
        self._stop_flag.set() # پرچم توقف را بالا ببر
        
        # توقف موتورهای DC
        self.set_dc_speed('pad', 0)
        self.set_dc_speed('lissa', 0)
        
        # منتظر بمان تا ترد حرکت ستون واقعاً متوقف شود
        if self._motion_thread and self._motion_thread.is_alive():
            self._motion_thread.join(timeout=0.5)
            
        self.state["is_moving"] = False

    def reset_stop_flag(self):
        """پایین آوردن پرچم توقف برای حرکت بعدی"""
        self._stop_flag.clear()

    # ==========================
    # توابع کنترل موتور DC
    # ==========================
    
    def set_dc_speed(self, motor_name: str, speed_percent: int):
        # 1. محدود سازی عدد بین 0 تا 100
        speed_percent = max(0, min(100, speed_percent))
        
        # 2. آپدیت وضعیت
        key_map = {'pad': 'pad_speed', 'lissa': 'lissa_speed', 'light': 'light_intensity'}
        if motor_name in key_map:
            self.state[key_map[motor_name]] = speed_percent

        # 3. اعمال به سخت‌افزار
        if IS_RASPBERRY_PI and motor_name in self.motors:
            self.motors[motor_name].value = speed_percent / 100.0
        else:
            # فقط جهت لاگ کردن در حالت شبیه‌سازی
            print(f"🔧 [SIM] {motor_name} speed -> {speed_percent}%")

    # ==========================
    # توابع پیشرفته استپر (Physics)
    # ==========================

    def move_column_raw(self, steps: int, direction: str):
        """
        لایه فیزیک: اجرای حرکت با بررسی لحظه‌به‌لحظه ترمز
        """
        self.state["is_moving"] = True
        
        # تنظیم جهت
        dir_val = 1 if direction == "up" else 0
        if IS_RASPBERRY_PI:
            self.motors['step_dir'].value = dir_val
        else:
            print(f"🔼 [SIM] START MOVE: {direction} ({steps} steps)")

        # حلقه اصلی حرکت
        for i in range(steps):
            # 1. چک کردن ترمز اضطراری (حیاتی!)
            if self._stop_flag.is_set():
                print("🛑 [MODEL] Motion aborted by user.")
                break

            # 2. محاسبه تاخیر (Ramping)
            delay = self._calculate_ramp_delay(i, steps)
            
            # 3. اعمال پالس
            if IS_RASPBERRY_PI:
                with self._hw_lock:
                    self.motors['step_pulse'].on()
                    # زمان روشن بودن پالس (خیلی کوتاه)
                    time.sleep(0.00001) 
                    self.motors['step_pulse'].off()
                    # زمان خاموش بودن (تعیین کننده سرعت)
                    time.sleep(delay)
            else:
                # شبیه‌سازی دقیق زمان‌بندی
                time.sleep(delay)

        self.state["is_moving"] = False
        if not IS_RASPBERRY_PI: print("⏹️ [SIM] Move finished.")

    def _calculate_ramp_delay(self, current_step, total_steps):
        """محاسبه دینامیک سرعت (منحنی S)"""
        # اگر کل مسیر کوتاه‌تر از باند شتاب است، باند را نصف کن
        ramp_len = min(self.RAMP_STEPS, total_steps // 2)
        
        if current_step < ramp_len:
            # شتاب مثبت (تند شدن)
            progress = current_step / ramp_len
            return self.MAX_PULSE_DELAY - (progress * (self.MAX_PULSE_DELAY - self.MIN_PULSE_DELAY))
        
        elif current_step > (total_steps - ramp_len):
            # شتاب منفی (کند شدن/ترمز نرم)
            steps_left = total_steps - current_step
            progress = steps_left / ramp_len
            return self.MAX_PULSE_DELAY - (progress * (self.MAX_PULSE_DELAY - self.MIN_PULSE_DELAY))
        
        else:
            # سرعت ثابت (کروز)
            return self.MIN_PULSE_DELAY

    def move_column_mm(self, dist_mm: int, direction: str):
        """
        لایه مدیریت ترد: تبدیل واحد و شروع حرکت امن
        """
        # اگر حرکت قبلی هنوز تمام نشده، اجازه حرکت جدید نده (مگر اینکه ترمز زده شود)
        if self.state["is_moving"]:
            print("⚠️ [MODEL] Busy! Ignoring command.")
            return

        # ریست کردن پرچم ترمز برای حرکت جدید
        self.reset_stop_flag()
        
        steps = int(dist_mm * self.STEPS_PER_MM)
        
        # شروع ترد جدید
        self._motion_thread = threading.Thread(target=self.move_column_raw, args=(steps, direction))
        self._motion_thread.daemon = True # با بسته شدن برنامه، این ترد هم بمیرد
        self._motion_thread.start()