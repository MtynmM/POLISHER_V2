import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const


BTN_PADDING = (20, 15)

class ControlPanel:
    def __init__(self, parent, control_widgets, title, unit, default_value, input_key):
       
        self.parent = parent
        self.widgets = control_widgets
        self.title = title
        self.unit = unit
        self.default_value = default_value
        self.input_key = input_key

        self._create_ui()

    def _create_ui(self):
        # 1. کانتینر اصلی
        container = ttk.Frame(self.parent)
        container.pack(expand=True)

        # 2. عنوان صفحه
        ttk.Label(container, text=self.title, font=("Segoe UI", 24, "bold")).pack(
            pady=20
        )

        # 3. ردیف کنترل‌ها
        controls = ttk.Frame(container)
        controls.pack(pady=10)

        # دکمه کاهش (-)
        btn_minus = ttk.Button(
            controls, text="−", bootstyle="warning", padding=BTN_PADDING
        )
        btn_minus.pack(side=ttk_const.LEFT, padx=20)

        # نمایشگر عدد
        lbl_value = ttk.Label(
            controls,
            text=self.default_value,
            font=("Segoe UI", 36, "bold"),
            bootstyle="inverse-secondary",
        )
        lbl_value.pack(side=ttk_const.LEFT, padx=30)

        # ذخیره لیبل با کلید اختصاصی
        self.widgets[self.input_key] = lbl_value

        # دکمه افزایش (+)
        btn_plus = ttk.Button(controls, text="+", bootstyle="success", padding=BTN_PADDING)
        btn_plus.pack(side=ttk_const.LEFT, padx=20)

        # 4. نمایش واحد
        ttk.Label(container, text=self.unit, font=("Segoe UI", 16)).pack(pady=10)

        # 5. دکمه ثبت (Apply)
        btn_apply = ttk.Button(
            container, text="ثبت (Apply)", bootstyle="primary", padding=BTN_PADDING
        )
        btn_apply.pack(pady=20)

        # ذخیره دکمه‌ها در جعبه ابزار مشترک
        self.widgets[f"{self.input_key}_minus"] = btn_minus
        self.widgets[f"{self.input_key}_plus"] = btn_plus
        self.widgets[f"{self.input_key}_apply"] = btn_apply
