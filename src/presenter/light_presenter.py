class LightPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # 1. دسترسی به ویجت‌ها
        self.slider = view.control_widgets["light_scale"]
        self.toggle = view.control_widgets["light_toggle"]
        
        # 2. اتصال رویدادها
        self.slider.configure(command=self.on_slider_change)
        self.toggle.configure(command=self.on_toggle_click)

    def on_slider_change(self, value):
        """وقتی اسلایدر حرکت می‌کند"""
        # [اصلاح 1] اول چک کن آیا دکمه چراغ روشن است؟
        # اگر دکمه پایین نباشد (selected نباشد)، فرمانی به سخت‌افزار نفرست
        if "selected" in self.toggle.state():
            try:
                brightness = int(float(value))
                self.model.set_brightness(brightness)
            except ValueError:
                pass

    def on_toggle_click(self):
        """وقتی دکمه روشن/خاموش زده می‌شود"""
        # [اصلاح 2] بررسی وضعیت دکمه (آیا الان روشن شد یا خاموش؟)
        if "selected" in self.toggle.state():
            # === حالت روشن (ON) ===
            # عدد فعلی اسلایدر را بخوان و اعمال کن
            current_val = int(self.slider.get())
            self.model.set_brightness(current_val)
        else:
            # === حالت خاموش (OFF) ===
            # نور را صفر کن (ولی اسلایدر را تکان نده تا حافظه بماند)
            self.model.set_brightness(0)