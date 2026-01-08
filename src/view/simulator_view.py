import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const
from ttkbootstrap.widgets import Meter
import math

class SimulatorView(ttk.Toplevel):
    """
    Advanced Hardware Simulator (Digital Twin)
    
    ویژگی‌ها:
    - شبیه‌سازی اینرسی موتور (Motor Inertia Simulation)
    - رابط کاربری صنعتی با استفاده از گیج‌های عقربه‌ای (Meter)
    - نمایشگر عمودی برای محور Z
    - جداسازی منطق UI از منطق به‌روزرسانی
    """
    
    # تنظیمات ثابت برای طراحی تمیزتر
    WINDOW_SIZE = "500x700+1050+50"
    REFRESH_RATE_MS = 30  # حدود 30 فریم بر ثانیه برای روانی حرکت
    SMOOTHING_FACTOR = 0.1 # ضریب نرمی حرکت (بین 0 و 1) - کمتر یعنی نرم‌تر/کندتر

    def __init__(self, model):
        super().__init__(title="Fiber Optic Polisher - Digital Twin")
        self.geometry(self.WINDOW_SIZE)
        self.resizable(False, False)
        self.model = model
        
        # متغیرهای داخلی برای شبیه‌سازی فیزیک (Current Values)
        self._current_pad_val = 0.0
        self._current_light_val = 0.0
        self._z_axis_phase = 0.0  # برای انیمیشن حرکت ستون
        
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        
        # ساختاردهی UI
        self._init_ui()
        
        # شروع حلقه مانیتورینگ
        self._start_simulation_loop()

    def _init_ui(self):
        """راه‌اندازی تمام اجزای گرافیکی"""
        # کانتینر اصلی با پدینگ
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=ttk_const.BOTH, expand=True)

        # 1. هدر وضعیت
        self._create_header(main_frame)
        
        ttk.Separator(main_frame).pack(fill=ttk_const.X, pady=15)

        # 2. داشبورد اصلی (موتور و ستون)
        self._create_dashboard(main_frame)

        # 3. کنترل نور
        self._create_light_control(main_frame)

        # 4. نوار وضعیت پایین
        self._create_statusbar()

    def _create_header(self, parent):
        lbl_title = ttk.Label(
            parent, 
            text="SYSTEM MONITORING", 
            font=("Impact", 18), 
            bootstyle="primary"
        )
        lbl_title.pack(anchor="w")
        
        self.lbl_connection = ttk.Label(
            parent, 
            text="● VIRTUAL LINK ACTIVE", 
            font=("Segoe UI", 9, "bold"), 
            bootstyle="success"
        )
        self.lbl_connection.pack(anchor="w")

    def _create_dashboard(self, parent):
        # استفاده از Grid برای چیدمان دو ستونی
        dash_frame = ttk.Frame(parent)
        dash_frame.pack(fill=ttk_const.BOTH, expand=True, pady=10)

        # --- ستون چپ: موتور پد (Meter) ---
        pad_frame = ttk.Labelframe(dash_frame, text=" Pad Rotation (RPM) ", padding=10, bootstyle="info")
        pad_frame.pack(side=ttk_const.LEFT, fill=ttk_const.BOTH, expand=True, padx=(0, 10))

        self.meter_pad = Meter(
            pad_frame,
            metersize=180,
            padding=5,
            amountused=0,
            metertype="semi",  # حالت نیم‌دایره
            subtext="Power %",
            interactive=False,
            bootstyle="info",
            textright="%",
            stripethickness=10
        )
        self.meter_pad.pack(pady=10)

        # --- ستون راست: موقعیت ستون (Z-Axis) ---
        col_frame = ttk.Labelframe(dash_frame, text=" Z-Axis Position ", padding=10, bootstyle="warning")
        col_frame.pack(side=ttk_const.RIGHT, fill=ttk_const.Y, padx=(0, 0))

        # کانتینر برای اسلایدر عمودی
        z_container = ttk.Frame(col_frame)
        z_container.pack(fill=ttk_const.Y, expand=True, anchor="center")

        self.scale_z = ttk.Scale(
            z_container, 
            from_=100, 
            to=0, 
            orient=ttk_const.VERTICAL, 
            bootstyle="warning",
            state="disabled" # کاربر نباید بتواند دستی تغییر دهد
        )
        self.scale_z.pack(side=ttk_const.LEFT, fill=ttk_const.Y, expand=True, ipady=20)
        
        # لیبل وضعیت حرکت
        self.lbl_z_status = ttk.Label(
            col_frame, 
            text="IDLE", 
            font=("Consolas", 10, "bold"), 
            bootstyle="secondary",
            anchor="center"
        )
        self.lbl_z_status.pack(side=ttk_const.BOTTOM, fill=ttk_const.X, pady=5)

    def _create_light_control(self, parent):
        lf_light = ttk.Labelframe(parent, text=" Ring Light Output ", padding=15)
        lf_light.pack(fill=ttk_const.X, pady=10)
        
        self.progress_light = ttk.Progressbar(
            lf_light, 
            maximum=100, 
            bootstyle="warning-striped", 
            value=0
        )
        self.progress_light.pack(fill=ttk_const.X, side=ttk_const.LEFT, expand=True)
        
        self.lbl_light_val = ttk.Label(lf_light, text="0%", width=4, anchor="center")
        self.lbl_light_val.pack(side=ttk_const.RIGHT, padx=5)

    def _create_statusbar(self):
        self.statusbar = ttk.Label(
            self, 
            text="System Ready | Waiting for commands...", 
            relief=ttk_const.SUNKEN, 
            anchor=ttk_const.W, 
            font=("Segoe UI", 9),
            padding=(10, 5),
            bootstyle="inverse-dark"
        )
        self.statusbar.pack(side=ttk_const.BOTTOM, fill=ttk_const.X)

    def _start_simulation_loop(self):
        """حلقه اصلی شبیه‌سازی با نرخ فریم ثابت"""
        if self.winfo_exists():
            self._update_physics()
            self._update_visuals()
            self.after(self.REFRESH_RATE_MS, self._start_simulation_loop)

    def _update_physics(self):
        """محاسبات ریاضی برای نرم‌کردن حرکات (شبیه‌سازی اینرسی)"""
        try:
            state = self.model.state
            
            # 1. Pad Motor Physics (Exponential Smoothing)
            # به جای پرش ناگهانی، به آرامی به سمت هدف میل می‌کند
            target_pad = state.get("pad_speed", 0)
            diff = target_pad - self._current_pad_val
            
            if abs(diff) > 0.5:
                # فرمول: مقدار جدید = مقدار قدیم + (تفاوت * ضریب)
                self._current_pad_val += diff * self.SMOOTHING_FACTOR
            else:
                self._current_pad_val = target_pad

            # 2. Light Physics (Faster response than motor)
            target_light = state.get("light_intensity", 0)
            self._current_light_val += (target_light - self._current_light_val) * 0.2

        except Exception as e:
            print(f"Simulation Physics Error: {e}")

    def _update_visuals(self):
        """به‌روزرسانی ویجت‌ها بر اساس مقادیر محاسبه شده"""
        try:
            state = self.model.state

            # --- بروزرسانی موتور پد ---
            val_int = int(self._current_pad_val)
            self.meter_pad.configure(amountused=val_int)
            
            # تغییر رنگ گیج بر اساس سرعت
            if val_int > 80: self.meter_pad.configure(bootstyle="danger")
            elif val_int > 0: self.meter_pad.configure(bootstyle="success")
            else: self.meter_pad.configure(bootstyle="info")

            # --- بروزرسانی نور ---
            self.progress_light['value'] = int(self._current_light_val)
            self.lbl_light_val.configure(text=f"{int(self._current_light_val)}%")

            # --- بروزرسانی محور Z (انیمیشن سینوسی) ---
            is_moving = state.get("is_moving", False)
            
            if is_moving:
                self.lbl_z_status.configure(text="MOVING", bootstyle="inverse-warning")
                self.statusbar.configure(text=f"Process Active | Motor: {val_int}% | Light: {int(self._current_light_val)}%")
                
                # ایجاد یک حرکت رفت و برگشتی نرم (Sine Wave) برای نشان دادن فعالیت
                # چون موقعیت واقعی سنسور را نداریم، یک حرکت مصنوعی تولید می‌کنیم
                self._z_axis_phase += 0.2
                oscillation = (math.sin(self._z_axis_phase) * 40) + 50 # نوسان بین 10 تا 90
                self.scale_z.configure(value=oscillation)
                
            else:
                self.lbl_z_status.configure(text="HOLD", bootstyle="inverse-secondary")
                self.statusbar.configure(text="System Idle")
                # بازگشت آرام به موقعیت Home (مثلا 0 یا 100) یا توقف در آخرین مکان
                # در اینجا شبیه‌ساز را در حالت سکون نگه می‌داریم

        except Exception as e:
            self.statusbar.configure(text=f"ERROR: {str(e)}", bootstyle="inverse-danger")