class ColumnPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # تلاش اولیه برای اتصال
        self.bind_events()

    def bind_events(self):
        """یافتن دکمه‌ها و اتصال رویدادها (قابل فراخوانی مجدد)"""
        # دریافت دکمه‌ها از دیکشنری (با نام‌های جدید پنل شیشه‌ای)
        self.btn_up = self.view.control_widgets.get("step_up")
        self.btn_down = self.view.control_widgets.get("step_down")
        
        # اتصال رویدادهای فشردن و رها کردن (Press & Hold)
        if self.btn_up:
            self.btn_up.bind('<ButtonPress-1>', self.start_move_up)
            self.btn_up.bind('<ButtonRelease-1>', self.stop_move)
            print("[OK] Column UP Button Connected")

        if self.btn_down:
            self.btn_down.bind('<ButtonPress-1>', self.start_move_down)
            self.btn_down.bind('<ButtonRelease-1>', self.stop_move)
            print("[OK] Column DOWN Button Connected")

    def start_move_up(self, event):
        self.model.move_up()
        # تغییر متن وضعیت پایین صفحه
        if hasattr(self.view, 'lbl_status_step'):
            self.view.lbl_status_step.configure(text="State: MOVING UP", bootstyle="inverse-warning")

    def start_move_down(self, event):
        self.model.move_down()
        if hasattr(self.view, 'lbl_status_step'):
            self.view.lbl_status_step.configure(text="State: MOVING DOWN", bootstyle="inverse-warning")

    def stop_move(self, event):
        self.model.stop()
        if hasattr(self.view, 'lbl_status_step'):
            self.view.lbl_status_step.configure(text="State: IDLE", bootstyle="inverse-secondary")