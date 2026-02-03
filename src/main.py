import sys
import time

# ایمپورت ماژول‌های پروژه
# نکته: مطمئن شوید فایل‌های __init__.py در پوشه‌ها وجود دارند تا ایمپورت کار کند
from view.main_view import PolisherView
from model.light_model import LightModel
from presenter.light_presenter import LightPresenter

# --- تنظیمات سخت‌افزار ---
PIN_LIGHT_GPIO = 18 #12 in rpi

def main():
    print("Starting Fiber Polisher System V2...")

    # 1. ساخت رابط کاربری (View)
    # پنجره ساخته می‌شود اما تا زمان اجرای mainloop نمایش داده نمی‌شود
    app = PolisherView()
    
    # 2. راه‌اندازی سخت‌افزار (Model)
    light_model = None
    try:
        print(f"Initializing Light Hardware on GPIO {PIN_LIGHT_GPIO}...")
        light_model = LightModel(pin_number=PIN_LIGHT_GPIO)
        
    except Exception as e:
        print(f"CRITICAL HARDWARE ERROR: {e}")
        print("Hint: Are you running on a Raspberry Pi with 'gpiozero' installed?")
        # در صورت خرابی سخت‌افزار، برنامه را می‌بندیم (یا می‌توانیم فقط خطا بدهیم)
        sys.exit(1)

    # 3. اتصال مغز متفکر (Presenter)
    # پرزینتر به صورت خودکار رویدادهای دکمه‌ها و اسلایدرها را مدیریت می‌کند
    try:
        presenter = LightPresenter(model=light_model, view=app)
        # در اینجا رفرنس پرزینتر را به ویو هم می‌دهیم (اختیاری، برای توسعه‌های آینده)
        app.set_presenter(presenter)
        print("Presenter linked successfully.")
        
    except KeyError as e:
        print(f"UI Binding Error: Widget {e} not found in View.")
        sys.exit(1)

    # 4. اجرای حلقه اصلی برنامه
    print("Showing GUI... (Press Ctrl+C to force quit)")
    try:
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\nForce stopping by user...")
        
    finally:
        # 5. تمیزکاری و خروج ایمن (Cleanup)
        print("Cleaning up resources...")
        if light_model:
            light_model.close()
        print("System shutdown complete. Goodbye!")

if __name__ == "__main__":
    main()