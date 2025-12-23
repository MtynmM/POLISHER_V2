import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

class ManualPanel:
    def __init__(self, parent, control_widgets):
        """
        پنل کنترل دستی (Manual Control)
        شامل: تنظیم ارتفاع، سرعت و نور
        """
        self.parent = parent
        self.widgets = control_widgets
        self.BTN_PADDING = (10, 10) # پدینگ داخلی دکمه‌ها
        
        self._create_ui()

    def _create_ui(self):
        # کانتینر اصلی که وسط‌چین باشد
        container = ttk.Frame(self.parent)
        container.pack(expand=True, fill=ttk_const.BOTH, padx=50, pady=20)
        
        # عنوان
        ttk.Label(container, text="⚙️ کنترل دستی (Manual Control)", font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        # 1. بخش تنظیم ارتفاع
        self._create_slider_row(container, "تنظیم ارتفاع (Height)", "manual_h")
        
        # 2. بخش تنظیم سرعت
        self._create_slider_row(container, "تنظیم سرعت (Speed)", "manual_s")

    def _create_slider_row(self, parent, title, key_prefix):
        """یک ردیف استاندارد شامل: دکمه منفی، اسلایدر، دکمه مثبت"""
        frame = ttk.Labelframe(parent, text=title, padding=15, bootstyle="info")
        frame.pack(fill=ttk_const.X, pady=10)

        box = ttk.Frame(frame)
        box.pack(fill=ttk_const.X)

        # دکمه کاهش
        btn_down = ttk.Button(box, text="−", width=5, bootstyle="warning", padding=self.BTN_PADDING)
        btn_down.pack(side=ttk_const.LEFT)

        # اسلایدر
        scale = ttk.Scale(box, from_=0, to=100, bootstyle="info")
        scale.pack(side=ttk_const.LEFT, fill=ttk_const.X, expand=True, padx=20)

        # دکمه افزایش
        btn_up = ttk.Button(box, text="+", width=5, bootstyle="success", padding=self.BTN_PADDING)
        btn_up.pack(side=ttk_const.LEFT)

        # ثبت ویجت‌ها در دیکشنری برای دسترسی Presenter
        self.widgets[f"{key_prefix}_down"] = btn_down
        self.widgets[f"{key_prefix}_scale"] = scale
        self.widgets[f"{key_prefix}_up"] = btn_up