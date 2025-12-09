import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

# --- ثابت‌های طراحی ---
TITLE_FONT = ("Segoe UI", 24, "bold")
VALUE_FONT = ("Segoe UI", 36, "bold")
UNIT_FONT = ("Segoe UI", 16)
KEYPAD_FONT = ("Segoe UI", 14, "bold")
BTN_PADDING = (15, 10)

class ControlPanel:
    def __init__(self, parent, control_widgets, title, unit, default_value, input_key):
        self.parent = parent
        self.widgets = control_widgets
        self.title = title
        self.unit = unit
        self.default_value = default_value
        self.input_key = input_key
        
        # متغیر موقت برای نگه داشتن عدد در حال تایپ
        self.current_value = str(default_value)

        self._create_ui()

    def _create_ui(self):
        # 1. کانتینر اصلی
        container = ttk.Frame(self.parent)
        container.pack(expand=True, fill=ttk_const.BOTH)

        # 2. بخش نمایشگر (بالا)
        display_frame = ttk.Frame(container)
        display_frame.pack(pady=10)

        ttk.Label(display_frame, text=self.title, font=TITLE_FONT).pack(pady=(10, 5))

        # نمایشگر عدد و دکمه‌های +/- (برای تنظیم دقیق)
        value_box = ttk.Frame(display_frame)
        value_box.pack(pady=5)

        btn_minus = ttk.Button(value_box, text="−", bootstyle="warning", padding=(15, 15))
        btn_minus.pack(side=ttk_const.LEFT, padx=15)

        # لیبل نمایش عدد
        self.lbl_value = ttk.Label(
            value_box,
            text=self.current_value,
            font=VALUE_FONT,
            bootstyle="inverse-secondary",
            width=6, anchor="center"
        )
        self.lbl_value.pack(side=ttk_const.LEFT, padx=10)
        
        # ذخیره لیبل
        self.widgets[self.input_key] = self.lbl_value

        btn_plus = ttk.Button(value_box, text="+", bootstyle="success", padding=(15, 15))
        btn_plus.pack(side=ttk_const.LEFT, padx=15)

        ttk.Label(display_frame, text=self.unit, font=UNIT_FONT).pack(pady=0)

        # 3. صفحه کلید عددی (Numpad)
        keypad_frame = ttk.Frame(container)
        keypad_frame.pack(pady=10)

        # چیدمان دکمه‌ها
        keys = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('C', 3, 0), ('0', 3, 1), ('OK', 3, 2)
        ]

        for key, row, col in keys:
            if key == 'OK':
                style = "primary"
                cmd = lambda: self._on_keypad_enter() # دکمه تایید (جایگزین Apply)
            elif key == 'C':
                style = "danger"
                cmd = lambda: self._on_keypad_clear()
            else:
                style = "secondary"
                cmd = lambda k=key: self._on_keypad_press(k)

            btn = ttk.Button(
                keypad_frame,
                text=key,
                bootstyle=style,
                width=4,
                padding=(8, 12),
                command=cmd
            )
            # دکمه OK را برای دسترسی Presenter ذخیره می‌کنیم (اگر نیاز به لاجیک خاص بود)
            if key == 'OK':
                 self.widgets[f"{self.input_key}_apply"] = btn
            
            btn.grid(row=row, column=col, padx=5, pady=5)

        # ذخیره دکمه‌های +/- برای پرزنتر
        self.widgets[f"{self.input_key}_minus"] = btn_minus
        self.widgets[f"{self.input_key}_plus"] = btn_plus

    # --- توابع داخلی کیبورد (Logic View) ---
    def _on_keypad_press(self, key):
        """وقتی عدد زده می‌شود"""
        if self.current_value == "0":
            self.current_value = key
        else:
            self.current_value += key
        self.lbl_value.config(text=self.current_value)

    def _on_keypad_clear(self):
        """پاک کردن (Backspace)"""
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
        self.lbl_value.config(text=self.current_value)
    
    def _on_keypad_enter(self):
        """
        وقتی OK زده شد، این تابع اجرا می‌شود.
        نکته: در معماری MVP، دکمه OK ما در self.widgets ذخیره شده
        و Presenter متد خودش را به آن وصل می‌کند.
        اما برای اینکه UI آپدیت شود، ما اینجا فعلا کاری نمی‌کنیم
        و می‌گذاریم Presenter فرمان نهایی را اجرا کند.
        (ولی چون کامند را اینجا lambda دادیم، باید آن را هندل کنیم یا 
        از طریق Presenter دکمه را configure کنیم).
        
        راه حل ساده: این دکمه OK الان به هیچ جا وصل نیست جز این تابع.
        ما باید در Presenter به این دکمه گوش دهیم.
        """
        # اینجا می‌توانیم یک افکت بصری بدهیم
        pass