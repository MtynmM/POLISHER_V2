import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const
from tkinter import messagebox
from .panels.timer_panel import TimerPanel
from .panels.control_panel import ControlPanel


class PolisherView(ttk.Window):
    """
    Polisher V2 - رابط کاربری اصلی
    """

    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Polisher V2")
        self.geometry("1024x600")
        self.resizable(False, False)
        self.overrideredirect(True)

        # 1. سیستم طراحی (Design System)
        self.BTN_PADDING = (15, 10)
        self.BTN_FONT = ("Segoe UI", 12, "bold")
        self.LBL_FONT = ("Segoe UI", 12)
        self.TITLE_FONT = ("Segoe UI", 14, "bold")
        self.TOOLBAR_PADX = 8
        self.TOOLBAR_PADY = 8
        self.BTN_PADX = 4
        self.BTN_PADY = 4
        self.STATUS_PADX = 9
        self.MENU_WIDTH = 250
        self.style.configure(
            "TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(10, 5)
        )

        # تنظیم استایل‌ها
        button_styles = [
            "primary",
            "danger",
            "info",
            "success",
            "light",
            "secondary",
            "warning",
        ]
        for style in button_styles:
            self.style.configure(f"{style}.TButton", font=self.BTN_FONT)
        self.style.configure("TLabel", font=self.LBL_FONT)

        # وضعیت منو
        self.menu_visible = False
        self.side_menu_pos = -self.MENU_WIDTH

        # 2. ساختار اصلی
        self._create_toolbar()
        self._create_status_bar()
        self._create_side_menu_drawer()  # منوی مخفی
        self._create_content_frame()

        # دیکشنری برای دسترسی به ویجت‌های کنترل (برای Presenter)
        self.control_widgets = {}
        self.presenter = None  # مدیر بعدا وصل می‌شود

    def set_presenter(self, presenter):
        self.presenter = presenter

    def _create_toolbar(self):
        """نوار ابزار بالا"""
        self.top_frame = ttk.Frame(self, bootstyle=ttk_const.SECONDARY)
        self.top_frame.pack(
            side=ttk_const.TOP,
            fill=ttk_const.X,
            padx=self.TOOLBAR_PADX,
            pady=self.TOOLBAR_PADY,
        )

        ttk.Label(
            self.top_frame, text="Polisher V2", font=("Segoe UI", 20, "bold")
        ).pack(side=ttk_const.RIGHT, padx=15)

        # دکمه منو
        self.btn_Menu = ttk.Button(
            self.top_frame,
            text="☰",
            bootstyle=ttk_const.PRIMARY,
            padding=self.BTN_PADDING,
            width=5,
            command=self._toggle_menu,
        )
        self.btn_Menu.pack(side=ttk_const.LEFT, padx=self.BTN_PADX, pady=self.BTN_PADY)

        # دکمه Home (تغییر جدید: اتصال به show_home_view)
        self.btn_Home = ttk.Button(
            self.top_frame,
            text="🏠 Home",
            bootstyle=ttk_const.PRIMARY,
            padding=self.BTN_PADDING,
            width=10,
            command=lambda: self.show_home_view(),  # <--- این خط اضافه شد
        )
        self.btn_Home.pack(side=ttk_const.LEFT, padx=self.BTN_PADX)

        self.btn_Save = ttk.Button(
            self.top_frame,
            text="💾 Save",
            bootstyle=ttk_const.PRIMARY,
            padding=self.BTN_PADDING,
            width=10,
        )
        self.btn_Save.pack(side=ttk_const.LEFT, padx=self.BTN_PADX)

    def _create_side_menu_drawer(self):
        """ساخت منوی کشویی (مخفی)"""
        self.side_menu_frame = ttk.Frame(self, bootstyle=ttk_const.DARK)

        # عنوان منو
        ttk.Label(
            self.side_menu_frame,
            text="Menu",
            font=self.TITLE_FONT,
            bootstyle="inverse-dark",
        ).pack(pady=20)

        # دکمه‌های منو
        menu_items = [
            ("📷 Camera", ttk_const.PRIMARY, lambda: self.show_camera_view()),
            ("⏱️ Timer", ttk_const.PRIMARY, lambda: self.show_timer_view()),
            ("⚙️ Manual", ttk_const.PRIMARY, lambda: self.show_manual_view()),
        ]
        for text, style, cmd in menu_items:
            ttk.Button(
                self.side_menu_frame,
                text=text,
                bootstyle=style,
                padding=self.BTN_PADDING,
                width=15,
                command=cmd,
            ).pack(pady=15, padx=20, fill=ttk_const.X)

        # دکمه‌های کنترل
        ttk.Button(
            self.side_menu_frame,
            text="👣 Step",
            bootstyle=ttk_const.PRIMARY,
            padding=self.BTN_PADDING,
            width=12,
            command=lambda: self.show_step_panel(),
        ).pack(pady=15, padx=20, fill=ttk_const.X)

        ttk.Button(
            self.side_menu_frame,
            text="🔄 Pad Rotation",
            bootstyle=ttk_const.PRIMARY,
            padding=self.BTN_PADDING,
            width=12,
            command=lambda: self.show_speed_panel(),
        ).pack(pady=5, padx=20, fill=ttk_const.X)

        # قرارگیری اولیه (مخفی)
        self.side_menu_frame.place(
            x=self.side_menu_pos, y=80, width=self.MENU_WIDTH, relheight=1
        )

    def _toggle_menu(self):
        """انیمیشن باز/بسته شدن منو"""
        if self.menu_visible:
            self._animate_menu(-self.MENU_WIDTH)  # مخفی کردن
            self.menu_visible = False
        else:
            self.side_menu_frame.lift()
            self._animate_menu(0)  # نمایش دادن
            self.menu_visible = True

    def _animate_menu(self, target_x):
        step = 40
        if self.side_menu_pos < target_x:
            self.side_menu_pos += step
            if self.side_menu_pos > target_x:
                self.side_menu_pos = target_x
        elif self.side_menu_pos > target_x:
            self.side_menu_pos -= step
            if self.side_menu_pos < target_x:
                self.side_menu_pos = target_x

        self.side_menu_frame.place(x=self.side_menu_pos)
        if self.side_menu_pos != target_x:
            self.after(10, lambda: self._animate_menu(target_x))

    def _create_content_frame(self):
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=ttk_const.BOTH, expand=True, padx=10, pady=10)
        self.show_home_view()

    def _create_status_bar(self):
        self.status_frame = ttk.Frame(self, bootstyle=ttk_const.SECONDARY)
        self.status_frame.pack(side=ttk_const.BOTTOM, fill=ttk_const.X)

        self.lbl_contact_light = ttk.Label(
            self.status_frame,
            text="█",  # کاراکتر دایره توپر
            font=(None, 15),  # سایز بزرگ تا شبیه چراغ شود
            bootstyle="danger",  # پیش‌فرض قرمز (قطع تماس)
        )
        self.lbl_contact_light.pack(
            side=ttk_const.RIGHT,
        )

        self.lbl_status_step = ttk.Label(
            self.status_frame, text="Step: 100", bootstyle="inverse-secondary"
        )
        self.lbl_status_step.pack(side=ttk_const.RIGHT, padx=20, pady=5)

        self.lbl_status_speed = ttk.Label(
            self.status_frame, text="Speed: 100 RPM", bootstyle="inverse-secondary"
        )
        self.lbl_status_speed.pack(side=ttk_const.RIGHT, padx=20, pady=5)

        self.lbl_status_angle = ttk.Label(
            self.status_frame, text="Angle: 0°", bootstyle="inverse-secondary"
        )
        self.lbl_status_angle.pack(side=ttk_const.RIGHT, padx=20, pady=5)

    # --- توابع نمایش پنل‌ها (جایگزین دیکشنری پیچیده) ---
    def _clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if self.menu_visible:
            self._toggle_menu()  # بستن خودکار منو

    def show_home_view(self):
        """نمایش صفحه اصلی (Home)"""
        self._clear_content()  # پاکسازی صفحه

        # ساخت محتوای صفحه خانه
        container = ttk.Frame(self.content_frame)
        container.pack(expand=True)

        ttk.Label(
            container,
            text="Polisher V2",
            font=("Segoe UI", 48, "bold"),
            bootstyle=ttk_const.PRIMARY,
        ).pack(pady=20)

        ttk.Label(
            container, text="لطفاً یک گزینه را از منو انتخاب کنید", font=("Segoe UI", 20)
        ).pack(pady=10)

    def show_step_panel(self):
        self._clear_content()
        ControlPanel(
            self.content_frame,
            self.control_widgets,
            "تنظیم گام (Step)",
            "میکرون",
            "100",
            "step",
        )

    def show_speed_panel(self):
        self._clear_content()
        ControlPanel(
            self.content_frame,
            self.control_widgets,
            "تنظیم سرعت (Speed)",
            "RPM",
            "100",
            "speed",
        )

    def show_camera_view(self):
        self._clear_content()
        ttk.Label(
            self.content_frame, text="نمای دوربین (Camera)", font=("Segoe UI", 24)
        ).pack(expand=True)

    def show_timer_view(self):
        """نمایش صفحه تایمر با دو تب (کرنومتر و تایمر معکوس)"""
        self._clear_content()

        TimerPanel(self.content_frame, self.control_widgets)

        # تابع کمکی برای ساختن ستون‌های +/- (جلوگیری از تکرار کد)
        def _create_time_column(label_text, key_name):
            frame = ttk.Frame(settings_frame)
            frame.pack(side=ttk_const.LEFT, padx=20)

            # عنوان (مثلاً "دقیقه")
            ttk.Label(frame, text=label_text, font=("Segoe UI", 12)).pack(pady=5)

            # دکمه مثبت (بالا)
            btn_up = ttk.Button(
                frame,
                text="▲",
                bootstyle="secondary-outline",
                width=5,
                padding=self.BTN_PADDING,
            )
            btn_up.pack(pady=2)

            # نمایشگر عدد
            lbl_val = ttk.Label(
                frame,
                text="00",
                font=("Segoe UI", 20, "bold"),
                bootstyle="inverse-secondary",
                width=3,
                anchor="center",
            )
            lbl_val.pack(pady=2)

            # دکمه منفی (پایین)
            btn_down = ttk.Button(
                frame,
                text="▼",
                bootstyle="secondary-outline",
                width=5,
                padding=self.BTN_PADDING,
            )
            btn_down.pack(pady=2)

            # ذخیره ویجت‌ها برای پرزنتر
            self.control_widgets[f"timer_{key_name}_lbl"] = lbl_val
            self.control_widgets[f"timer_{key_name}_up"] = btn_up
            self.control_widgets[f"timer_{key_name}_down"] = btn_down

        # ساخت سه ستون با استفاده از تابع بالا
        _create_time_column("ساعت", "h")
        _create_time_column("دقیقه", "m")
        _create_time_column("ثانیه", "s")

        # 2. نمایشگر زمان کل (برای وقتی که تایمر شروع شد)
        self.lbl_countdown = ttk.Label(
            container,
            text="00:00:00",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary",
        )
        self.lbl_countdown.pack(pady=2)
        self.control_widgets["timer_total_display"] = self.lbl_countdown

        # 3. دکمه‌های شروع/توقف
        action_frame = ttk.Frame(container)
        action_frame.pack(pady=10)

        btn_start = ttk.Button(
            action_frame, text="▶ Start", bootstyle="primary", padding=self.BTN_PADDING
        )
        btn_start.pack(side=ttk_const.LEFT, padx=10)

        btn_stop = ttk.Button(
            action_frame, text="⏸ Stop", bootstyle="primary", padding=self.BTN_PADDING
        )
        btn_stop.pack(side=ttk_const.LEFT, padx=10)

        btn_reset = ttk.Button(
            action_frame, text="⟳ Reset", bootstyle="primary", padding=self.BTN_PADDING
        )
        btn_reset.pack(side=ttk_const.LEFT, padx=10)

        # ذخیره دکمه‌های اصلی
        self.control_widgets["timer_start"] = btn_start
        self.control_widgets["timer_stop"] = btn_stop
        self.control_widgets["timer_reset"] = btn_reset

    def show_manual_view(self):
        self._clear_content()
        self._build_manual_panel()

    def _build_manual_panel(self):
        """ساخت پنل تنظیمات دستی (اسلایدرها و نور)"""
        container = ttk.Frame(self.content_frame)
        container.pack(expand=True, fill=ttk_const.BOTH, padx=50, pady=20)

        # 1. کنترل ارتفاع
        self._create_slider_row(container, "تنظیم ارتفاع (Height)", "manual_h")

        # 2. کنترل سرعت
        self._create_slider_row(container, "تنظیم سرعت (Speed)", "manual_s")

        # 3. کنترل نور (Light)
        light_frame = ttk.Labelframe(
            container,
            text="کنترل نور (Light)",
            padding=self.BTN_PADDING,
            bootstyle="warning",
        )
        light_frame.pack(fill=ttk_const.X, pady=10)

        chk_light = ttk.Checkbutton(
            light_frame, text="خاموش / روشن", bootstyle="success-round-toggle"
        )
        chk_light.pack(pady=5)
        self.control_widgets["manual_light_toggle"] = chk_light

    def _create_slider_row(self, parent, title, key_prefix):
        """تابع کمکی برای ساخت ردیف اسلایدر"""
        frame = ttk.Labelframe(
            parent, text=title, padding=self.BTN_PADDING, bootstyle="info"
        )
        frame.pack(fill=ttk_const.X, pady=10)

        box = ttk.Frame(frame)
        box.pack(fill=ttk_const.X)

        btn_down = ttk.Button(
            box, text="−", width=5, bootstyle="warning", padding=self.BTN_PADDING
        )
        btn_down.pack(side=ttk_const.LEFT)

        scale = ttk.Scale(box, from_=0, to=100, bootstyle="info")
        scale.pack(side=ttk_const.LEFT, fill=ttk_const.X, expand=True, padx=20)

        btn_up = ttk.Button(
            box, text="+", width=5, bootstyle="success", padding=self.BTN_PADDING
        )
        btn_up.pack(side=ttk_const.LEFT)

        # ذخیره در دیکشنری برای Presenter
        self.control_widgets[f"{key_prefix}_down"] = btn_down
        self.control_widgets[f"{key_prefix}_scale"] = scale
        self.control_widgets[f"{key_prefix}_up"] = btn_up

    def show_timer_view(self):
        """نمایش صفحه تایمر (با استفاده از کلاس جداگانه)"""
        self._clear_content()
        # ساخت نمونه از کلاس جدید و سپردن مسئولیت به آن
        TimerPanel(self.content_frame, self.control_widgets)

    def set_contact_status(self, is_touching: bool):
        """
        تغییر رنگ چراغ وضعیت اتصال
        True -> سبز (در حال تماس)
        False -> قرمز (آزاد)
        """
        if is_touching:
            self.lbl_contact_light.configure(bootstyle="success")  # سبز
        else:
            self.lbl_contact_light.configure(bootstyle="danger")  # قرمز
