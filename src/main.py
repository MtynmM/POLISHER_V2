import sys

# ایمپورت ماژول‌های پروژه
# نکته: مطمئن شوید فایل‌های __init__.py در پوشه‌ها وجود دارند تا ایمپورت کار کند
from view.main_view import PolisherView

from model.light_model import LightModel
from model.lissa_model import LissaModel
from presenter.light_presenter import LightPresenter
from presenter.lissa_presenter import LissaPresenter
from model.pad_model import PadModel
from presenter.pad_presenter import PadPresenter
from model.column_model import ColumnModel
from presenter.column_presenter import ColumnPresenter

# --- تنظیمات سخت‌افزار ---
PIN_LIGHT_GPIO = 18 #light
PIN_LISSA_GPIO = 26 #lissa

#pins for pad
PIN_PAD_PWM = 12
PIN_PAD_CW = 13
PIN_PAD_CCW = 6

#pins for column
PIN_COL_PWM = 19
PIN_COL_DIR = 5

def main():
    print("Starting Fiber Polisher System V2...")

    # 1. ساخت رابط کاربری (View)
    # پنجره ساخته می‌شود اما تا زمان اجرای mainloop نمایش داده نمی‌شود
    app = PolisherView()
    
    # 2. راه‌اندازی سخت‌افزار (Model)
    light_model = None
    lissa_model = None
    pad_model = None
    col_model = None

    try:
        light_model = LightModel(pin_number=PIN_LIGHT_GPIO)
        lissa_model = LissaModel(pin_number=PIN_LISSA_GPIO)
        pad_model = PadModel(pwm_pin = PIN_PAD_PWM, cw_pin = PIN_PAD_CW, ccw_pin = PIN_PAD_CCW)
        col_model = ColumnModel(en_pin=PIN_COL_PWM, dir_pin=PIN_COL_DIR)

    except Exception as e:
        print(f"HARDWARE ERROR: {e}")
        # در صورت خرابی سخت‌افزار، برنامه را می‌بندیم (یا می‌توانیم فقط خطا بدهیم)
        sys.exit(1)

    # 3. اتصال مغز متفکر (Presenter)
    # پرزینتر به صورت خودکار رویدادهای دکمه‌ها و اسلایدرها را مدیریت می‌کند
    try:
        p_light = LightPresenter(model=light_model, view=app)
        p_lissa = LissaPresenter(model=lissa_model, view=app)
        p_pad = PadPresenter(model=pad_model, view=app)
        p_col = ColumnPresenter(model=col_model, view=app)


        # در اینجا رفرنس پرزینتر را به ویو هم می‌دهیم (اختیاری، برای توسعه‌های آینده)
        app.set_presenter(light_presenter = p_light, lissa_presenter = p_lissa, pad_presenter = p_pad, column_presenter = p_col)
        print("Presenter linked successfully.")
        
    except KeyError as e:
        print(f"UI Binding Error: Widget {e} not found in View.")
        sys.exit(1)

    # 4. اجرای حلقه اصلی برنامه
    print("Showing GUI...")
    try:
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\nForce stopping by user...")
    finally:
        # 5. تمیزکاری و خروج ایمن (Cleanup)
        print("Cleaning up resources...")
        if col_model: col_model.close()
        if pad_model: pad_model.close()
        if light_model: light_model.close()
        if lissa_model: lissa_model.close()
        print("System shutdown complete. Goodbye!")

if __name__ == "__main__":
    main()