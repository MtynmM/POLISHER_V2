import time
import threading
import ttkbootstrap as ttk
from view.simulator_view import SimulatorView  # کلاسی که در مرحله قبل ساختیم

class MockModel:
    """
    این کلاس نقش دیتابیس یا وضعیت لحظه‌ای دستگاه را بازی می‌کند.
    در واقعیت، این مقادیر از سنسورهای سخت‌افزاری خوانده می‌شوند.
    """
    def __init__(self):
        # این دیکشنری دقیقاً همان state است که ویو منتظر آن است
        self.state = {
            "pad_speed": 0,        # سرعت موتور پد (0-100)
            "light_intensity": 0,  # شدت نور (0-100)
            "is_moving": False     # آیا ستون در حال حرکت است؟
        }

def run_test_scenario(model, app):
    """
    این تابع یک سناریوی تست خودکار را اجرا می‌کند.
    شبیه به کاری که یک اپراتور با دستگاه انجام می‌دهد.
    """
    print("🚀 TEST STARTED: Simulation Sequence Initiated...")
    
    # 1. حالت آماده‌باش (Idle)
    time.sleep(1)
    
    # 2. روشن کردن نور (Soft Start)
    print("--> Phase 1: Lights On")
    for i in range(0, 101, 5):
        model.state["light_intensity"] = i
        time.sleep(0.05)
        
    # 3. استارت موتور (Ramp Up)
    print("--> Phase 2: Motor Start")
    for i in range(0, 85, 2): # تا 85 درصد سرعت می‌گیریم
        model.state["pad_speed"] = i
        time.sleep(0.05)
        
    # 4. شروع حرکت محور Z (Machining Process)
    print("--> Phase 3: Z-Axis Movement (Processing)")
    model.state["is_moving"] = True
    # نگه داشتن وضعیت برای 5 ثانیه
    time.sleep(5)
    
    # 5. توقف اضطراری یا پایان کار (Cool Down)
    print("--> Phase 4: Stopping Process")
    model.state["is_moving"] = False
    
    # کاهش سرعت موتور
    while model.state["pad_speed"] > 0:
        model.state["pad_speed"] -= 5
        time.sleep(0.1)
    
    model.state["pad_speed"] = 0
    print("✅ TEST COMPLETED. Closing in 3 seconds...")
    
    time.sleep(3)
    app.destroy() # بستن پنجره

if __name__ == "__main__":
    # 1. ساخت مدل تقلبی
    shared_model = MockModel()
    
    # 2. راه‌اندازی برنامه اصلی UI
    app = ttk.Window(title="Main Controller", themename="darkly")
    app.withdraw() # پنجره اصلی را مخفی می‌کنیم چون فقط شبیه‌ساز را می‌خواهیم
    
    # 3. ایجاد و نمایش پنجره شبیه‌ساز
    # نکته مهم: مدل را به ویو تزریق می‌کنیم (Dependency Injection)
    sim_view = SimulatorView(shared_model)
    
    # 4. اجرای سناریوی تست در یک ترد (Thread) جداگانه
    # چرا ترد؟ چون اگر در ترد اصلی (Main Thread) باشیم، رابط کاربری فریز می‌شود!
    test_thread = threading.Thread(target=run_test_scenario, args=(shared_model, sim_view))
    test_thread.daemon = True # با بسته شدن برنامه، این ترد هم بسته شود
    test_thread.start()
    
    # 5. شروع حلقه اصلی رابط کاربری
    print("GUI is running...")
    sim_view.mainloop()