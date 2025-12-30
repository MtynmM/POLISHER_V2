import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const
from tkinter import messagebox

# ایمپورت ماژولار پنل‌ها
from .panels.timer_panel import TimerPanel
from .panels.control_panel import ControlPanel
from .panels.manual_panel import ManualPanel

class PolisherView(ttk.Window):
    """
    Polisher V2 Professional - HMI (Diamond Edition)
    طراحی شده برای نمایشگر لمسی 7 اینچ (1024x600)
    ویژگی‌ها: بدون کد اضافه، رابط کاربری صنعتی، بهینه شده.
    """
    
    # === سیستم طراحی (Design System) ===
    CONSTANTS = {
        "WIN_SIZE": "1024x600",
        "MENU_WIDTH": 260,     # عرض منو
        "TOOLBAR_HEIGHT": 80,  # ارتفاع هدر
        "FOOTER_HEIGHT": 45,   # ارتفاع فوتر
        "FONT_H1": ("Segoe UI", 22, "bold"),
        "FONT_H2": ("Segoe UI", 14, "bold"),
        "FONT_BODY": ("Segoe UI", 11),
        "BTN_PAD": (15, 10),
    }

    def __init__(self):
        super().__init__(themename="darkly")
        
        # 1. تنظیمات پنجره (Window Config)
        self.title("Polisher V2 Pro")
        self.geometry(self.CONSTANTS["WIN_SIZE"])
        self.resizable(False, False)
        self.overrideredirect(True) # تمام صفحه (Kiosk Mode)

        # 2. وضعیت‌های داخلی
        self.menu_visible = False
        self.side_menu_pos = -self.CONSTANTS["MENU_WIDTH"]
        self.control_widgets = {} # مخزن ویجت‌ها برای Presenter
        self.presenter = None

        # 3. راه‌اندازی گرافیک
        self._setup_styles()
        self._build_layout()
        
        # 4. رندر نهایی
        self.update_idletasks()

    def set_presenter(self, presenter):
        """اتصال به مغز متفکر (Presenter)"""
        self.presenter = presenter

    def _setup_styles(self):
        """تعریف استایل‌های اختصاصی"""
        style = self.style
        
        # دکمه‌های نوار بالا
        style.configure("TopBar.TButton", font=("Segoe UI", 11, "bold"))
        
        # دکمه‌های منوی کناری (نام Sidebar برای جلوگیری از تداخل نام)
        style.configure("Sidebar.TButton", font=("Segoe UI", 12, "bold"))
        
        # تب‌ها و اسلایدر
        style.configure("TNotebook.Tab", font=("Segoe UI", 12), padding=(15, 8))
        style.configure("TScale", sliderlength=30, sliderthickness=20)
        
        # استایل لیبل LED وضعیت
        style.configure("Led.TLabel", font=("Arial", 12, "bold"), padding=(10, 5))

    def _build_layout(self):
        """چیدمان اصلی صفحه"""
        # 1. کانتینر اصلی
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=ttk_const.BOTH, expand=True)

        # 2. نوار ابزار (Top)
        self._create_toolbar()
        
        # 3. نوار وضعیت (Bottom)
        self._create_status_bar()
        
        # 4. کانتینر محتوا (Middle)
        self.main_container = ttk.Frame(self.content_frame)
        
        # محاسبه دقیق ارتفاع
        top_h = self.CONSTANTS["TOOLBAR_HEIGHT"]
        foot_h = self.CONSTANTS["FOOTER_HEIGHT"]
        content_h = 600 - top_h - foot_h - 5 
        
        self.main_container.place(x=0, y=top_h, relwidth=1, height=content_h)

        # 5. منوی کشویی (Overlay)
        self._create_side_menu()

        # نمایش صفحه پیش‌فرض
        self.show_home_view()

    # ==========================================
    # اجزای رابط کاربری (UI Components)
    # ==========================================

    def _create_toolbar(self):
        bar = ttk.Frame(self, bootstyle=ttk_const.SECONDARY)
        bar.place(x=0, y=0, relwidth=1, height=self.CONSTANTS["TOOLBAR_HEIGHT"])

        # دکمه منو
        self.btn_Menu = ttk.Button(
            bar, text="MENU", bootstyle=ttk_const.PRIMARY,
            style="TopBar.TButton", padding=self.CONSTANTS["BTN_PAD"],
            command=self._toggle_menu
        )
        self.btn_Menu.pack(side=ttk_const.LEFT, padx=15, pady=10)

        # دکمه خانه
        self.btn_Home = ttk.Button(
            bar, text="HOME", bootstyle=ttk_const.INFO,
            style="TopBar.TButton", padding=self.CONSTANTS["BTN_PAD"],
            command=self.show_home_view
        )
        self.btn_Home.pack(side=ttk_const.LEFT, padx=5, pady=10)

        # دکمه ذخیره تنظیمات
        self.btn_Save = ttk.Button(
            bar, text="SAVE CONFIG", bootstyle=ttk_const.SUCCESS,
            style="TopBar.TButton", padding=self.CONSTANTS["BTN_PAD"]
        )
        self.btn_Save.pack(side=ttk_const.LEFT, padx=5, pady=10)
        self.control_widgets['btn_save'] = self.btn_Save

        # دکمه خروج
        ttk.Button(
            bar, text="EXIT", bootstyle=ttk_const.DANGER,
            style="TopBar.TButton", padding=self.CONSTANTS["BTN_PAD"],
            command=self.quit
        ).pack(side=ttk_const.RIGHT, padx=15, pady=10)

        # عنوان
        ttk.Label(
            bar, text="POLISHER PRO", 
            font=self.CONSTANTS["FONT_H1"], 
            bootstyle="inverse-secondary"
        ).pack(side=ttk_const.RIGHT, padx=20)

    def _create_status_bar(self):
        """نوار وضعیت پایینی"""
        bar = ttk.Frame(self, bootstyle=ttk_const.SECONDARY)
        bar.pack(side=ttk_const.BOTTOM, fill=ttk_const.X, ipady=2)

        # دکمه کنترل نور
        self.chk_light = ttk.Checkbutton(bar, text="Light", bootstyle="warning-toolbutton")
        self.chk_light.pack(side=ttk_const.LEFT, padx=10, pady=3)
        self.control_widgets["light_toggle"] = self.chk_light

        # اسلایدر نور
        self.scale_light = ttk.Scale(bar, from_=0, to=100, bootstyle="warning", length=300)
        self.scale_light.pack(side=ttk_const.LEFT, padx=15, pady=8)
        self.control_widgets["light_scale"] = self.scale_light

        # چراغ وضعیت اتصال (به صورت LED مجازی)
        # استفاده از inverse-danger باعث می‌شود پس‌زمینه قرمز شود (مثل چراغ)
        self.lbl_contact_light = ttk.Label(
            bar, text="NO CONTACT", 
            style="Led.TLabel",
            bootstyle="inverse-danger",
            width=12, anchor="center"
        )
        self.lbl_contact_light.pack(side=ttk_const.RIGHT, padx=15)

        # نمایشگرهای عددی
        self.lbl_status_step = ttk.Label(bar, text="Step: ---", font=self.CONSTANTS["FONT_BODY"], bootstyle="inverse-secondary")
        self.lbl_status_step.pack(side=ttk_const.RIGHT, padx=15)
        
        self.lbl_status_speed = ttk.Label(bar, text="Speed: 0%", font=self.CONSTANTS["FONT_BODY"], bootstyle="inverse-secondary")
        self.lbl_status_speed.pack(side=ttk_const.RIGHT, padx=15)

    def _create_side_menu(self):
        """منوی کشویی"""
        self.side_menu = ttk.Frame(self, bootstyle=ttk_const.DARK)
        
        ttk.Label(
            self.side_menu, text="NAVIGATION", 
            font=self.CONSTANTS["FONT_H2"], 
            bootstyle="inverse-dark"
        ).pack(pady=25)

        menu_items = [
            ("Timer / Stopwatch", "primary", self.show_timer_view),
            ("Set Step Size",     ttk_const.SECONDARY, self.show_step_panel),
            ("Set Speed Step",    ttk_const.SUCCESS, self.show_speed_panel),
            ("Camera View",       ttk_const.DANGER,  self.show_camera_view),
        ]

        for text, style, cmd in menu_items:
            btn_frame = ttk.Frame(self.side_menu, bootstyle=style)
            btn_frame.pack(fill=ttk_const.X, padx=15, pady=8)
            
            ttk.Button(
                btn_frame, text=text, 
                bootstyle=style,
                style="Sidebar.TButton",
                command=lambda c=cmd: self._handle_menu_click(c)
            ).pack(fill=ttk_const.X, ipady=8)

        # تنظیم مکان اولیه (مخفی)
        top_offset = self.CONSTANTS["TOOLBAR_HEIGHT"]
        menu_height = 600 - top_offset
        
        self.side_menu.place(
            x=self.side_menu_pos, 
            y=top_offset, 
            width=self.CONSTANTS["MENU_WIDTH"], 
            height=menu_height
        )

    # ==========================================
    # منطق UI (Logic)
    # ==========================================

    def _toggle_menu(self):
        target = 0 if not self.menu_visible else -self.CONSTANTS["MENU_WIDTH"]
        self.menu_visible = not self.menu_visible
        if self.menu_visible: self.side_menu.lift() 
        self._animate_menu(target)

    def _animate_menu(self, target_x):
        if self.side_menu_pos != target_x:
            dist = target_x - self.side_menu_pos
            step = dist / 4
            if abs(step) < 1: step = 1 if dist > 0 else -1
            if abs(dist) < 2: self.side_menu_pos = target_x
            else: self.side_menu_pos += step
            self.side_menu.place(x=int(self.side_menu_pos))
            self.after(10, lambda: self._animate_menu(target_x))

    def _handle_menu_click(self, command):
        self._toggle_menu()
        command()

    def _clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # ==========================================
    # نمایش صفحات (Navigation)
    # ==========================================

    def show_home_view(self):
        self._clear_main_container()
        if self.menu_visible: self._toggle_menu()
        
        container = ttk.Frame(self.main_container)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(container, text="SYSTEM READY", font=("Segoe UI", 48, "bold")).pack()
        ttk.Label(container, text="Select Mode from Menu", font=self.CONSTANTS["FONT_H2"]).pack(pady=10)

    def show_manual_panel(self):
        self._clear_main_container()
        ManualPanel(self.main_container, self.control_widgets)

    def show_timer_view(self):
        self._clear_main_container()
        TimerPanel(self.main_container, self.control_widgets)

    def show_step_panel(self):
        self._clear_main_container()
        ControlPanel(self.main_container, self.control_widgets, "Movement Step (um)", "100", "step")

    def show_speed_panel(self):
        self._clear_main_container()
        ControlPanel(self.main_container, self.control_widgets, "Speed Step (%)", "10", "speed")
        
    def show_camera_view(self):
        self._clear_main_container()
        lbl = ttk.Label(self.main_container, text="Camera Feed\n(No Signal)", font=self.CONSTANTS["FONT_H1"])
        lbl.pack(expand=True)

    # ==========================================
    # API ارتباطی
    # ==========================================
    def set_contact_status(self, is_touching: bool):
        """تغییر وضعیت LED مجازی تماس"""
        # اگر تماس برقرار است، سبز شود (CONTACT)
        # اگر تماس نیست، قرمز شود (NO CONTACT)
        if is_touching:
            self.lbl_contact_light.configure(bootstyle="inverse-success", text="CONTACT OK")
        else:
            self.lbl_contact_light.configure(bootstyle="inverse-danger", text="NO CONTACT")
            
    def show_info_message(self, message):
        """نمایش پیام موقت در نوار وضعیت (برای ذخیره تنظیمات)"""
        original_text = self.lbl_status_step.cget("text")
        self.lbl_status_step.configure(text=message, bootstyle="inverse-success")
        # بعد از 2 ثانیه به حالت قبل برگردد
        self.after(2000, lambda: self.lbl_status_step.configure(text=original_text, bootstyle="inverse-secondary"))