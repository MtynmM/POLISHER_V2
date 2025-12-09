import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const

# --- ثابت‌های طراحی ---
TIME_FONT = ("Segoe UI", 50, "bold")
COL_VAL_FONT = ("Segoe UI", 20, "bold")
BTN_PADDING_MAIN = (11, 11)
BTN_PADDING_SMALL = (12, 12) # برای دکمه‌های تنظیم دقیق

class TimerPanel:
    def __init__(self, parent_frame, control_widgets_dict):
        self.parent = parent_frame
        self.widgets = control_widgets_dict
        self._create_ui()

    def _create_ui(self):
        # 1. ساخت تب‌ها
        # نکته: استایل تب‌ها باید در main_view.py تنظیم شود، نه اینجا
        notebook = ttk.Notebook(self.parent, bootstyle="primary")
        notebook.pack(fill=ttk_const.BOTH, expand=True, padx=25, pady=10)
        
        stopwatch_frame = ttk.Frame(notebook, padding=20)
        timer_frame = ttk.Frame(notebook, padding=20)
        
        notebook.add(stopwatch_frame, text="⏱️ کرنومتر (Stopwatch)")
        notebook.add(timer_frame, text="⏲️ تایمر (Countdown)")
        
        self._create_stopwatch(stopwatch_frame)
        self._create_countdown(timer_frame)

    def _create_stopwatch(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill=ttk_const.BOTH,expand=True)
        
        lbl_time = ttk.Label(
            container, 
            text="00:00:00", 
            font=TIME_FONT, 
            bootstyle="primary",
            anchor="center"
        )
        lbl_time.pack(pady=30,fill=ttk_const.X)
        self.widgets["stopwatch_label"] = lbl_time
        
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=20)
        
        self._add_btn(btn_frame, "▶ Start", "success", "stopwatch_start")
        self._add_btn(btn_frame, "⏸ Stop", "warning", "stopwatch_stop")
        self._add_btn(btn_frame, "Reset", "danger", "stopwatch_reset")

    def _create_countdown(self, parent):
        container = ttk.Frame(parent)
        container.pack(expand=True, fill=ttk_const.BOTH)

        settings_frame = ttk.Frame(container)
        settings_frame.pack(pady=10)

        self._create_time_column(settings_frame, "ساعت", "h")
        self._create_time_column(settings_frame, "دقیقه", "m")
        self._create_time_column(settings_frame, "ثانیه", "s")

        lbl_countdown = ttk.Label(
            container, 
            text="00:00:00", 
            font=("Segoe UI", 20, "bold"), 
            anchor='center'
        )
        lbl_countdown.pack(pady=5)
        self.widgets["timer_total_display"] = lbl_countdown

        action_frame = ttk.Frame(container)
        action_frame.pack(pady=5, fill=ttk_const.Y)

        self._add_btn(action_frame, "▶ Start", "success", "timer_start")
        self._add_btn(action_frame, "⏸ Stop", "warning", "timer_stop")
        self._add_btn(action_frame, "Reset", "danger", "timer_reset")

    def _create_time_column(self, parent, label_text, key_name):
        frame = ttk.Frame(parent)
        frame.pack(side=ttk_const.LEFT, padx=20)
        
        ttk.Label(frame, text=label_text, font=("Segoe UI", 12)).pack(pady=5)
        
        # دکمه بالا
        btn_up = ttk.Button(frame, text="▲", bootstyle="secondary-outline", width=5, padding=BTN_PADDING_SMALL)
        btn_up.pack(pady=2)
        
        lbl_val = ttk.Label(
            frame, text="00", 
            font=COL_VAL_FONT, 
            bootstyle="inverse-secondary", 
            width=3, anchor="center"
        )
        lbl_val.pack(pady=5)
        
        # دکمه پایین
        btn_down = ttk.Button(frame, text="▼", bootstyle="secondary-outline", width=5, padding=BTN_PADDING_SMALL)
        btn_down.pack(pady=2)
        
        self.widgets[f"timer_{key_name}_lbl"] = lbl_val
        self.widgets[f"timer_{key_name}_up"] = btn_up
        self.widgets[f"timer_{key_name}_down"] = btn_down

    def _add_btn(self, parent, text, style, key):
        btn = ttk.Button(parent, text=text, bootstyle=style, padding=BTN_PADDING_MAIN)
        btn.pack(side=ttk_const.LEFT, padx=15)
        self.widgets[key] = btn