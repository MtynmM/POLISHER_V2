class PadPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # در ابتدا سعی می‌کنیم وصل شویم
        self.bind_events()

    def bind_events(self):
        """یافتن دکمه‌ها و اتصال رویدادها (قابل فراخوانی مجدد)"""
        # دریافت مجدد ویجت‌ها از دیکشنری
        self.btn_start = self.view.control_widgets.get("speed_start")
        self.btn_stop = self.view.control_widgets.get("speed_stop")
        self.btn_ccw = self.view.control_widgets.get("speed_dir")
        self.lbl_speed = self.view.control_widgets.get("speed")

        # اتصال رویدادها
        if self.btn_start:
            self.btn_start.configure(command=self.on_start)

        if self.btn_stop:
            self.btn_stop.configure(command=self.on_stop)

        if self.btn_ccw:
            self.btn_ccw.configure(command=self.on_dir_toggle)

    def on_start(self):
        """شروع حرکت موتور"""
        try:
            if self.lbl_speed: # چک کردن وجود لیبل
                speed_text = self.lbl_speed.cget("text")
                speed_val = int(speed_text)
                
                # اول جهت را ست می‌کنیم
                self.on_dir_toggle()
                
                # سپس سرعت را اعمال می‌کنیم
                self.model.set_speed(speed_val)
                
                # آپدیت وضعیت
                self.view.lbl_status_speed.configure(text=f"Speed: {speed_val}%", bootstyle="inverse-success")
                
        except ValueError:
            print("[ERROR] Invalid speed value")

    def on_stop(self):
        """توقف کامل"""
        self.model.set_speed(0)
        self.model.stop_rotation()
        self.view.lbl_status_speed.configure(text="Speed: 0%", bootstyle="inverse-danger")

    def on_dir_toggle(self):
        """تغییر جهت چرخش"""
        if self.btn_ccw:
            is_ccw = "selected" in self.btn_ccw.state()
            
            if is_ccw:
                # متن دکمه هم باید ساده باشد اگر فونت سیستم ساپورت نکند
                # اما معمولاً GUI مشکلی ندارد، فقط ترمینال مشکل دارد.
                # فعلا متن دکمه را با فلش نگه می‌داریم چون Tkinter معمولاً UTF-8 است.
                self.btn_ccw.configure(text="CCW <", bootstyle="outline-warning-toolbutton")
            else:
                self.btn_ccw.configure(text="CW >", bootstyle="outline-secondary-toolbutton")
            
            self.model.set_direction(is_ccw)