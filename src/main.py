import sys
import os
import logging

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# ایمپورت ماژول‌های پروژه
from model.main_model import MainModel, IS_RASPBERRY_PI
from view.main_view import PolisherView
from presenter.main_presenter import MainPresenter

# ایمپورت شبیه‌ساز (فقط برای تست لپ‌تاپ)
if not IS_RASPBERRY_PI:
    from view.simulator_view import SimulatorView

if __name__ == "__main__":
    try:
        logging.info("🚀 SYSTEM STARTUP INITIALIZED")
        
        # 1. ساخت مدل (قلb تپنده)
        model = MainModel()
        
        # 2. ساخت ویو (رابط کاربری)
        view = PolisherView()
        
        # 3. [مهم] اگر روی لپ‌تاپ هستیم، شبیه‌ساز را اجرا کن
        if not IS_RASPBERRY_PI:
            print("\n💻 SIMULATION MODE DETECTED: Launching Hardware Dashboard...\n")
            sim_view = SimulatorView(model)
        
        # 4. ساخت پرزنتر (مغز متفکر)
        presenter = MainPresenter(view, model)
        
        # 5. اجرا
        view.mainloop()

    except Exception as e:
        logging.critical(f"FATAL ERROR: {e}", exc_info=True)