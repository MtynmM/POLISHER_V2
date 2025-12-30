import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

class TimerPanel:
    """
    Polisher V2 - Timer & Stopwatch Panel (Diamond Edition)
    رابط کاربری زمان‌سنجی با دکمه‌های بزرگ و بهینه برای تاچ.
    """
    def __init__(self, parent_frame, control_widgets_dict):
        self.parent = parent_frame
        self.widgets = control_widgets_dict
        
        # تنظیمات ابعاد دکمه‌ها
        self.SPINNER_BTN_WIDTH = 6
        self.ACTION_BTN_WIDTH = 12
        
        self._create_ui()

    def _create_ui(self):
        # استفاده از تب (Notebook) برای تفکیک کرنومتر و تایمر
        # استایل primary برای تب‌ها استفاده می‌شود تا با تم دارک هماهنگ باشد
        notebook = ttk.Notebook(self.parent, bootstyle="primary")
        notebook.pack(fill=ttk_const.BOTH, expand=True, padx=20, pady=10)
        
        # تب 1: کرنومتر
        stopwatch_tab = ttk.Frame(notebook, padding=20)
        notebook.add(stopwatch_tab, text="⏱️ STOPWATCH")
        
        # تب 2: شمارش معکوس
        timer_tab = ttk.Frame(notebook, padding=20)
        notebook.add(timer_tab, text="⏲️ COUNTDOWN")
        
        # ساخت محتوای تب‌ها
        self._create_stopwatch_tab(stopwatch_tab)
        self._create_countdown_tab(timer_tab)

    def _create_stopwatch_tab(self, parent):
        """طراحی تب کرنومتر: تمرکز روی نمایشگر بزرگ"""
        # 1. نمایشگر زمان (بسیار بزرگ)
        lbl_time = ttk.Label(
            parent, 
            text="00:00:00", 
            font=("Segoe UI", 70, "bold"), # فونت غول‌پیکر برای خوانایی از دور
            bootstyle="inverse-dark",
            anchor="center"
        )
        lbl_time.pack(expand=True, fill=ttk_const.BOTH, pady=(20, 40))
        
        # ثبت برای Presenter
        self.widgets["stopwatch_label"] = lbl_time
        
        # 2. دکمه‌های کنترل (پایین صفحه)
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=ttk_const.X, pady=10)
        
        # دکمه شروع
        self._add_action_btn(btn_frame, "▶ START", "success", "stopwatch_start")
        # دکمه توقف
        self._add_action_btn(btn_frame, "⏸ STOP", "warning", "stopwatch_stop")
        # دکمه ریست
        self._add_action_btn(btn_frame, "↺ RESET", "danger", "stopwatch_reset")

    def _create_countdown_tab(self, parent):
        """طراحی تب شمارش معکوس: تنظیم راحت زمان"""
        # 1. بخش تنظیم زمان (H : M : S) - وسط چین
        setup_container = ttk.Frame(parent)
        setup_container.pack(expand=True, pady=10)

        # اسپینر ساعت
        self._create_spinner(setup_container, "HOURS", "h", max_val=23)
        # جداکننده (:)
        self._create_separator(setup_container)
        # اسپینر دقیقه
        self._create_spinner(setup_container, "MINS", "m", max_val=59)
        # جداکننده (:)
        self._create_separator(setup_container)
        # اسپینر ثانیه
        self._create_spinner(setup_container, "SECS", "s", max_val=59)

        # 2. نمایشگر زمان کل (زیر تنظیمات)
        # این لیبل وقتی تایمر شروع شد آپدیت می‌شود
        lbl_total = ttk.Label(
            parent, 
            text="READY TO START", 
            font=("Segoe UI", 20, "bold"), 
            anchor="center",
            bootstyle="info"
        )
        lbl_total.pack(pady=(0, 20))
        self.widgets["timer_total_display"] = lbl_total

        # 3. دکمه‌های کنترل
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=ttk_const.X, pady=10)

        self._add_action_btn(action_frame, "▶ START", "success", "timer_start")
        self._add_action_btn(action_frame, "⏸ STOP", "warning", "timer_stop")
        self._add_action_btn(action_frame, "↺ RESET", "danger", "timer_reset")

    def _create_spinner(self, parent, label_text, key_suffix, max_val):
        """یک ویجت تنظیم عدد با دکمه‌های بزرگ بالا/پایین"""
        frame = ttk.Frame(parent)
        frame.pack(side=ttk_const.LEFT, padx=10)
        
        # دکمه افزایش (بالا)
        btn_up = ttk.Button(
            frame, text="▲", 
            bootstyle="secondary-outline", 
            width=self.SPINNER_BTN_WIDTH,
            padding=(5, 10) # ارتفاع مناسب برای لمس
        )
        btn_up.pack(pady=2)
        
        # نمایش عدد
        lbl_val = ttk.Label(
            frame, text="00", 
            font=("Segoe UI", 28, "bold"), 
            width=3, anchor="center"
        )
        lbl_val.pack(pady=5)
        
        # دکمه کاهش (پایین)
        btn_down = ttk.Button(
            frame, text="▼", 
            bootstyle="secondary-outline", 
            width=self.SPINNER_BTN_WIDTH,
            padding=(5, 10)
        )
        btn_down.pack(pady=2)
        
        # لیبل راهنما (مثلاً Hours)
        ttk.Label(frame, text=label_text, font=("Segoe UI", 9), bootstyle="secondary").pack(pady=2)
        
        # ثبت در ویجت‌ها برای Presenter
        self.widgets[f"timer_{key_suffix}_up"] = btn_up
        self.widgets[f"timer_{key_suffix}_down"] = btn_down
        self.widgets[f"timer_{key_suffix}_lbl"] = lbl_val

    def _create_separator(self, parent):
        """دو نقطه جداکننده ساعت و دقیقه"""
        ttk.Label(
            parent, text=":", 
            font=("Segoe UI", 28, "bold"), 
            bootstyle="secondary",
            padding=(0, 20) # تنظیم ارتفاع برای هم‌ترازی با اعداد
        ).pack(side=ttk_const.LEFT, padx=5)

    def _add_action_btn(self, parent, text, style, key):
        """دکمه عملیاتی استاندارد و هم‌اندازه"""
        btn = ttk.Button(
            parent, 
            text=text, 
            bootstyle=style, 
            width=self.ACTION_BTN_WIDTH,
            padding=(10, 15) # دکمه حجیم
        )
        # استفاده از expand=True و side=LEFT برای تقسیم مساوی فضا
        btn.pack(side=ttk_const.LEFT, padx=10, expand=True, fill=ttk_const.X)
        self.widgets[key] = btn