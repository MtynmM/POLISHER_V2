import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

class ControlPanel:
    def __init__(self, parent, control_widgets, title, default_value, input_key, mode="position"):
        """
        Industrial Control Panel (Ultimate Edition)
        طراحی مدرن شیشه‌ای (Glassy) با حذف دکمه‌های اضافه.
        """
        self.parent = parent
        self.widgets = control_widgets
        self.title = title
        self.current_value = str(default_value)
        self.input_key = input_key
        self.mode = mode

        # --- تنظیمات استایل و عملکرد (Config) ---
        self.CONFIG = {
            "speed": {
                "theme": "info",
                # استایل outline-danger یعنی شیشه‌ای قرمز
                "btn_1": ("⏹ STOP", "outline-danger", "stop"), 
                # استایل outline-success یعنی شیشه‌ای سبز
                "btn_2": ("▶ START", "outline-success", "start"),
                "has_dir": True,
                "unit": "%"
            },
            "position": {
                "theme": "warning",
                "btn_1": ("▲ UP", "outline-warning", "up"),
                "btn_2": ("▼ DOWN", "outline-warning", "down"),
                "has_dir": False,
                "unit": "μm"
            }
        }
        
        self.cfg = self.CONFIG.get(mode, self.CONFIG["position"])
        self._create_ui()

    def _create_ui(self):
        """ساخت رابط کاربری مینیمال و صنعتی"""
        container = ttk.Frame(self.parent)
        container.pack(expand=True, fill=ttk_const.BOTH, padx=30, pady=15)

        # 1. تیتر (HEADER)
        ttk.Label(
            container, 
            text=self.title.upper(), 
            font=("Segoe UI", 11, "bold"), 
            bootstyle="secondary",
            anchor="center"
        ).pack(fill=ttk_const.X, pady=(0, 5))

        # 2. نمایشگر دیجیتال (LCD DISPLAY)
        self._create_lcd_display(container)

        # 3. نوار فرمان (ACTION BAR)
        self._create_action_bar(container)

        # خط جداکننده محو
        ttk.Separator(container, bootstyle="secondary").pack(fill=ttk_const.X, pady=15)

        # 4. کیبورد عددی (NUMPAD)
        self._create_numpad(container)

    def _create_lcd_display(self, parent):
        """باکس نمایشگر عدد با استایل LCD"""
        lcd_frame = ttk.Frame(parent)
        lcd_frame.pack(fill=ttk_const.X, pady=5)

        # عدد بزرگ و خوانا
        self.lbl_value = ttk.Label(
            lcd_frame, 
            text=self.current_value, 
            font=("Consolas", 48, "bold"), # فونت مونو اسپیس
            bootstyle="inverse-dark",      # بک‌گراند مشکی
            anchor="center",
            padding=(10, 10)
        )
        self.lbl_value.pack(fill=ttk_const.X, expand=True)
        
        # ثبت ویجت برای دسترسی Presenter
        self.widgets[self.input_key] = self.lbl_value

    def _create_action_bar(self, parent):
        """دکمه‌های کنترلی اصلی (شیشه‌ای)"""
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=ttk_const.X, pady=10)

        # دکمه سمت چپ (STOP / UP)
        btn_1_txt, btn_1_style, btn_1_key = self.cfg["btn_1"]
        b1 = ttk.Button(
            action_frame, 
            text=btn_1_txt, 
            bootstyle=btn_1_style, 
            width=8, 
            padding=15 # ارتفاع مناسب برای لمس
        )
        b1.pack(side=ttk_const.LEFT, expand=True, fill=ttk_const.X, padx=(0, 5))
        self.widgets[f"{self.input_key}_{btn_1_key}"] = b1

        # دکمه جهت (مخصوص مد Speed)
        if self.cfg["has_dir"]:
            # دکمه‌ای که وقتی خاموش است (CW) خاکستری است
            # و وقتی روشن می‌شود (CCW) قرمز/نارنجی می‌شود تا هشدار دهد جهت عکس است
            self.chk_dir = ttk.Checkbutton(
                action_frame, 
                text="↺ CCW",      # متن ثابت
                bootstyle="outline-warning-toolbutton", # استایل شیشه‌ای هشدار دهنده
                width=6,
                padding=(15, 15),
                command=self._on_dir_toggle # فقط برای لاگ یا تغییر ظاهر
            )
            self.chk_dir.pack(side=ttk_const.LEFT, padx=5)
            self.widgets[f"{self.input_key}_dir"] = self.chk_dir

        # دکمه سمت راست (START / DOWN)
        btn_2_txt, btn_2_style, btn_2_key = self.cfg["btn_2"]
        b2 = ttk.Button(
            action_frame, 
            text=btn_2_txt, 
            bootstyle=btn_2_style, 
            width=8, 
            padding=15
        )
        b2.pack(side=ttk_const.LEFT, expand=True, fill=ttk_const.X, padx=(5, 0))
        self.widgets[f"{self.input_key}_{btn_2_key}"] = b2

    def _create_numpad(self, parent):
        """کیبورد عددی بازطراحی شده (بدون OK)"""
        pad_frame = ttk.Frame(parent)
        pad_frame.pack(expand=True, fill=ttk_const.BOTH)

        # شبکه 3 ستونی
        for i in range(3): pad_frame.columnconfigure(i, weight=1)
        # 4 ردیف
        for i in range(4): pad_frame.rowconfigure(i, weight=1)

        # چیدمان دکمه‌ها
        keys = [
            ('7',0,0), ('8',0,1), ('9',0,2),
            ('4',1,0), ('5',1,1), ('6',1,2),
            ('1',2,0), ('2',2,1), ('3',2,2),
            # ردیف آخر: پاک کردن و صفر بزرگ
            ('Clr',3,0), ('0',3,1) 
        ]

        for k, r, c in keys:
            # استایل پیش‌فرض شیشه‌ای خاکستری
            st = "outline-secondary"
            cmd = lambda key=k: self._update_val(key)
            
            # تنظیمات خاص
            colspan = 1
            if k == 'Clr':
                st = "outline-danger" # قرمز شیشه‌ای
                cmd = lambda: self._update_val("0", clear=True)
            elif k == '0':
                colspan = 2 # صفر، دو خانه را اشغال کند (چون OK حذف شد)

            btn = ttk.Button(pad_frame, text=k, bootstyle=st, command=cmd)
            btn.grid(
                row=r, column=c, 
                columnspan=colspan, # ادغام ستون‌ها برای دکمه 0
                padx=4, pady=4, 
                sticky="nsew", # کش آمدن در تمام جهت‌ها
                ipady=10
            )

    def _update_val(self, char, clear=False):
        """به‌روزرسانی عدد نمایشگر"""
        if clear:
            self.current_value = "0"
        else:
            if self.current_value == "0": self.current_value = char
            elif len(self.current_value) < 4: self.current_value += char
        
        self.lbl_value.configure(text=self.current_value)

    def _on_dir_toggle(self):
        """تغییر ظاهری دکمه جهت (اختیاری)"""
        # اینجا لاجیک خاصی نیاز نیست چون Checkbutton خودش state را نگه می‌دارد.
        # فقط اگر بخواهیم متن را عوض کنیم اینجا می‌نویسیم.
        # فعلا ثابت "CCW" می‌ماند که اگر روشن شد یعنی CCW فعال است.
        pass