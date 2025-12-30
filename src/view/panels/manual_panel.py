import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

class ManualPanel:
    """
    Polisher V2 - Manual Control Panel (Diamond Edition)
    کنترل دستی موتورها با رابط کاربری صنعتی و ارگونومیک.
    """
    def __init__(self, parent, control_widgets):
        self.parent = parent
        self.widgets = control_widgets
        
        # تنظیمات تاچ (Touch Config)
        self.BTN_WIDTH = 6       # عرض دکمه‌ها
        self.BTN_PADDING = (15, 15) # پدینگ داخلی دکمه‌ها (بزرگ برای انگشت)
        
        self._create_ui()

    def _create_ui(self):
        # کانتینر اصلی با حاشیه مناسب
        container = ttk.Frame(self.parent)
        container.pack(expand=True, fill=ttk_const.BOTH, padx=30, pady=20)
        
        # تیتر صفحه
        ttk.Label(
            container, 
            text="MANUAL OPERATION", 
            font=("Segoe UI", 18, "bold"),
            bootstyle="info"
        ).pack(pady=(0, 25))

        # 1. بخش کنترل ارتفاع ستون (Stepper Motor)
        # نکته مهندسی: چون حرکت عمودی است، از فلش‌های بالا/پایین استفاده می‌کنیم
        self._create_stepper_controls(container)
        
        # فاصله بین دو بخش
        ttk.Separator(container, orient='horizontal').pack(fill='x', pady=20)

        # 2. بخش کنترل سرعت چرخش (Pad Motor)
        # نکته مهندسی: چون تنظیم مقدار است، از - و + استفاده می‌کنیم
        self._create_speed_controls(container)

    def _create_stepper_controls(self, parent):
        """بخش کنترل حرکت عمودی ستون"""
        frame = ttk.Labelframe(parent, text=" Column Position (Vertical) ", padding=15, bootstyle="secondary")
        frame.pack(fill=ttk_const.X, pady=5)

        # کانتینر داخلی
        box = ttk.Frame(frame)
        box.pack(fill=ttk_const.X)

        # دکمه پایین (Down)
        btn_down = ttk.Button(
            box, 
            text="▼ DOWN", # متن واضح + جهت
            bootstyle="warning", 
            width=10,
            padding=self.BTN_PADDING
        )
        btn_down.pack(side=ttk_const.LEFT, padx=10)
        
        # متن راهنما در وسط
        info_lbl = ttk.Label(
            box, 
            text="JOG CONTROL", 
            font=("Segoe UI", 12, "bold"),
            bootstyle="inverse-secondary",
            anchor="center",
            width=15
        )
        info_lbl.pack(side=ttk_const.LEFT, expand=True)

        # دکمه بالا (Up)
        btn_up = ttk.Button(
            box, 
            text="▲ UP", 
            bootstyle="warning", 
            width=10,
            padding=self.BTN_PADDING
        )
        btn_up.pack(side=ttk_const.RIGHT, padx=10)

        # ثبت در ویجت‌ها (مطابق با Presenter)
        self.widgets["manual_h_down"] = btn_down
        self.widgets["manual_h_up"] = btn_up

    def _create_speed_controls(self, parent):
        """بخش کنترل سرعت موتور پد"""
        frame = ttk.Labelframe(parent, text=" Pad Rotation Speed ", padding=15, bootstyle="secondary")
        frame.pack(fill=ttk_const.X, pady=5)

        box = ttk.Frame(frame)
        box.pack(fill=ttk_const.X)

        # دکمه کاهش (-)
        btn_dec = ttk.Button(
            box, 
            text="−", # علامت منفی ریاضی
            bootstyle="danger", 
            width=self.BTN_WIDTH,
            padding=self.BTN_PADDING
        )
        btn_dec.pack(side=ttk_const.LEFT, padx=10)

        # اسلایدر سرعت (Slider)
        scale = ttk.Scale(
            box, 
            from_=0, 
            to=100, 
            bootstyle="info",
            style="TScale" # استفاده از استایل ضخیم تعریف شده در MainView
        )
        scale.pack(side=ttk_const.LEFT, fill=ttk_const.X, expand=True, padx=25)

        # دکمه افزایش (+)
        btn_inc = ttk.Button(
            box, 
            text="+", # علامت مثبت ریاضی
            bootstyle="success", 
            width=self.BTN_WIDTH,
            padding=self.BTN_PADDING
        )
        btn_inc.pack(side=ttk_const.RIGHT, padx=10)

        # ثبت در ویجت‌ها
        self.widgets["manual_s_down"] = btn_dec
        self.widgets["manual_s_up"] = btn_inc
        self.widgets["manual_s_scale"] = scale