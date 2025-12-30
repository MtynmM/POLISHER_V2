import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

class ControlPanel:
    def __init__(self, parent, control_widgets, title, default_value, input_key):
        """
        پنل ورودی عددی (Numpad) - بهینه شده برای تاچ
        """
        self.parent = parent
        self.widgets = control_widgets
        self.title = title
        self.default_value = str(default_value)
        self.input_key = input_key
        self.current_value = self.default_value

        self._create_ui()

    def _create_ui(self):
        container = ttk.Frame(self.parent)
        container.pack(expand=True, fill=ttk_const.BOTH, padx=20)

        # --- بخش 1: نمایشگر و تیتر (بالا) ---
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=ttk_const.X, pady=(10, 5))

        ttk.Label(
            header_frame, 
            text=self.title, 
            font=("Segoe UI", 16, "bold"),
            anchor="center"
        ).pack()

        # باکس نمایش عدد + دکمه‌های تنظیم دقیق
        display_box = ttk.Frame(header_frame)
        display_box.pack(pady=10)

        # دکمه -
        btn_minus = ttk.Button(display_box, text="stop", bootstyle="warning-outline", width=6, padding=10)
        btn_minus.pack(side=ttk_const.LEFT, padx=10)

        # خود عدد
        self.lbl_value = ttk.Label(
            display_box,
            text=self.current_value,
            font=("Segoe UI", 32, "bold"), # فونت بزرگ و خوانا
            bootstyle="inverse-secondary",
            width=5, 
            anchor="center"
        )
        self.lbl_value.pack(side=ttk_const.LEFT, padx=10)
        
        # ذخیره لیبل برای آپدیت توسط پرزنتر
        self.widgets[self.input_key] = self.lbl_value

        # دکمه +
        btn_plus = ttk.Button(display_box, text="start", bootstyle="success-outline", width=6, padding=10)
        btn_plus.pack(side=ttk_const.LEFT, padx=10)

        # ثبت دکمه‌های فاین تیونینگ
        self.widgets[f"{self.input_key}_minus"] = btn_minus
        self.widgets[f"{self.input_key}_plus"] = btn_plus

        # --- بخش 2: کیبورد عددی (پایین) ---
        keypad_frame = ttk.Frame(container)
        keypad_frame.pack(expand=True, fill=ttk_const.BOTH, pady=5)

        # شبکه دکمه‌ها (Grid)
        keys = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('Clr', 3, 0), ('0', 3, 1), ('OK', 3, 2)
        ]

        # تنظیم وزن ستون‌ها و ردیف‌ها برای پر کردن فضا
        for i in range(3): keypad_frame.columnconfigure(i, weight=1)
        for i in range(4): keypad_frame.rowconfigure(i, weight=1)

        for key, row, col in keys:
            style = "secondary"
            cmd = lambda k=key: self._on_keypad_press(k)

            if key == 'OK':
                style = "primary" # دکمه سبز/آبی
                # دکمه OK را به متد داخلی وصل نمی‌کنیم، پرزنتر آن را مدیریت می‌کند
                # اما برای اینکه کار کند، فعلا خالی می‌گذاریم یا به یک متد دامی وصل می‌کنیم
                cmd = None 
            elif key == 'Clr':
                style = "danger"
                cmd = self._on_keypad_clear

            btn = ttk.Button(
                keypad_frame,
                text=key,
                bootstyle=style,
                command=cmd
            )
            # دکمه‌ها تمام فضای سلول را پر کنند (Sticky NSEW)
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

            # ثبت دکمه OK
            if key == 'OK':
                self.widgets[f"{self.input_key}_apply"] = btn

    def _on_keypad_press(self, key):
        """لاجیک داخلی: آپدیت عدد روی صفحه هنگام تایپ"""
        if self.current_value == "0":
            self.current_value = key
        else:
            if len(self.current_value) < 4: # محدودیت ۴ رقم
                self.current_value += key
        self.lbl_value.configure(text=self.current_value)

    def _on_keypad_clear(self):
        """پاک کردن عدد"""
        self.current_value = "0"
        self.lbl_value.configure(text=self.current_value)