import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

class ControlPanel:
    def __init__(self, parent, control_widgets, title, default_value, input_key, mode="position"):
        """
        پنل ورودی هوشمند
        mode: می‌تواند 'position' (برای حرکت) یا 'speed' (برای سرعت) باشد.
        """
        self.parent = parent
        self.widgets = control_widgets
        self.title = title
        self.default_value = str(default_value)
        self.input_key = input_key
        self.current_value = self.default_value

        # شرط‌گذاری بر اساس متغیر امن mode
        if mode == "speed":
            self.btn_minus_text = "⏹ STOP"
            self.btn_minus_style = "danger"
            self.btn_plus_text = "▶ START"
            self.btn_plus_style = "success"
        else:
            # حالت position (پیش‌فرض)
            self.btn_minus_text = "▲ UP"
            self.btn_minus_style = "warning"
            self.btn_plus_text = "▼ DOWN"
            self.btn_plus_style = "warning"

        # [حیاتی] این خط باعث نمایش پنل می‌شود. اگر نباشد صفحه سفید می‌ماند!
        self._create_ui()

    def _create_ui(self):
        container = ttk.Frame(self.parent)
        container.pack(expand=True, fill=ttk_const.BOTH, padx=20)

        # --- بخش 1: نمایشگر و تیتر ---
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=ttk_const.X, pady=(10, 5))

        ttk.Label(
            header_frame, text=self.title, 
            font=("Segoe UI", 16, "bold"), anchor="center"
        ).pack()

        display_box = ttk.Frame(header_frame)
        display_box.pack(pady=10)

        # دکمه سمت چپ
        btn_minus = ttk.Button(
            display_box, text=self.btn_minus_text, 
            bootstyle=self.btn_minus_style, width=12, padding=10
        )
        btn_minus.pack(side=ttk_const.LEFT, padx=10)

        # نمایشگر عدد
        self.lbl_value = ttk.Label(
            display_box, text=self.current_value,
            font=("Segoe UI", 32, "bold"), 
            bootstyle="inverse-secondary", width=5, anchor="center"
        )
        self.lbl_value.pack(side=ttk_const.LEFT, padx=10)
        self.widgets[self.input_key] = self.lbl_value

        # دکمه سمت راست
        btn_plus = ttk.Button(
            display_box, text=self.btn_plus_text, 
            bootstyle=self.btn_plus_style, width=12, padding=10
        )
        btn_plus.pack(side=ttk_const.LEFT, padx=10)

        # ثبت دکمه‌ها برای Presenter
        self.widgets[f"{self.input_key}_minus"] = btn_minus
        self.widgets[f"{self.input_key}_plus"] = btn_plus

        # --- بخش 2: کیبورد عددی ---
        keypad_frame = ttk.Frame(container)
        keypad_frame.pack(expand=True, fill=ttk_const.BOTH, pady=5)

        keys = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('Clr', 3, 0), ('0', 3, 1), ('OK', 3, 2)
        ]

        for i in range(3): keypad_frame.columnconfigure(i, weight=1)
        for i in range(4): keypad_frame.rowconfigure(i, weight=1)

        for key, row, col in keys:
            style = "secondary"
            cmd = lambda k=key: self._on_keypad_press(k)

            if key == 'OK':
                style = "primary"
                cmd = None 
            elif key == 'Clr':
                style = "danger"
                cmd = self._on_keypad_clear

            btn = ttk.Button(keypad_frame, text=key, bootstyle=style, command=cmd)
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

            if key == 'OK':
                self.widgets[f"{self.input_key}_apply"] = btn

    def _on_keypad_press(self, key):
        if self.current_value == "0": self.current_value = key
        else:
            if len(self.current_value) < 4: self.current_value += key
        self.lbl_value.configure(text=self.current_value)

    def _on_keypad_clear(self):
        self.current_value = "0"
        self.lbl_value.configure(text=self.current_value)