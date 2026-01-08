import threading
import time

class MainPresenter:
    """
    مغز متفکر برنامه (The Brain) - نسخه نهایی عملیاتی
    ویژگی‌ها: کنترل مستقیم موتورها، سناریوی اتوماتیک تایمر و عقب‌نشینی خودکار.
    """
    
    # تنظیم فاصله عقب‌نشینی خودکار پس از پایان کار (میلی‌متر)
    RETRACT_DIST_MM = 5.0 

    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # حافظه موقت برای تنظیمات تایمر
        self.timer_setup = {"h": 0, "m": 0, "s": 0}

        # 1. تزریق وابستگی
        self.view.set_presenter(self)

        # 2. استراتژی رهگیری (اتصال هوشمند دکمه‌ها)
        self.view.show_timer_view = self._wrap_navigation(
            self.view.show_timer_view, self._bind_timer_signals
        )
        self.view.show_step_panel = self._wrap_navigation(
            self.view.show_step_panel, self._bind_step_signals
        )
        self.view.show_speed_panel = self._wrap_navigation(
            self.view.show_speed_panel, self._bind_speed_signals
        )

        # 3. اتصال دکمه‌های ثابت
        self._bind_global_signals()

        # 4. شروع حلقه آپدیت رابط کاربری
        self._start_ui_loop()

    def _wrap_navigation(self, original_method, binder_method):
        """دکوریتور برای اتصال سیگنال‌ها پس از تغییر صفحه"""
        def wrapper():
            original_method()
            binder_method()
        return wrapper

    # ==========================================
    # بخش سیم‌کشی (Signal Binding)
    # ==========================================

    def _bind_global_signals(self):
        w = self.view.control_widgets
        if "btn_save" in w:
            w["btn_save"].configure(command=self.handle_save_config)
        if "light_toggle" in w:
            w["light_toggle"].configure(command=self.handle_light_toggle)
        if "light_scale" in w:
            w["light_scale"].configure(command=lambda v: self.handle_light_change(v))

    def _bind_timer_signals(self):
        w = self.view.control_widgets
        
        # کرنومتر
        if "stopwatch_start" in w: w["stopwatch_start"].configure(command=self.start_stopwatch)
        if "stopwatch_stop" in w: w["stopwatch_stop"].configure(command=self.stop_stopwatch)
        if "stopwatch_reset" in w: w["stopwatch_reset"].configure(command=self.reset_stopwatch)

        # تایمر معکوس (اتصال به سناریوی جدید)
        if "timer_start" in w: w["timer_start"].configure(command=self.start_timer_sequence)
        if "timer_stop" in w: w["timer_stop"].configure(command=self.stop_timer)
        if "timer_reset" in w: w["timer_reset"].configure(command=self.reset_timer)

        # دکمه‌های تنظیم زمان (اسپینرها)
        for unit in ["h", "m", "s"]:
            if f"timer_{unit}_up" in w:
                w[f"timer_{unit}_up"].configure(command=lambda u=unit: self._adjust_timer_setting(u, 1))
            if f"timer_{unit}_down" in w:
                w[f"timer_{unit}_down"].configure(command=lambda u=unit: self._adjust_timer_setting(u, -1))

        self._refresh_timer_setup_ui()

    def _bind_step_signals(self):
        w = self.view.control_widgets
        # دکمه Apply: ذخیره عدد
        if "step_apply" in w:
            w["step_apply"].configure(command=self.apply_step_config)
            
        # دکمه + (DOWN): حرکت به پایین
        if "step_plus" in w:
            w["step_plus"].configure(command=lambda: self.move_manual("down"))
            
        # دکمه - (UP): حرکت به بالا
        if "step_minus" in w:
            w["step_minus"].configure(command=lambda: self.move_manual("up"))

    def _bind_speed_signals(self):
        w = self.view.control_widgets
        # دکمه Apply: ذخیره عدد
        if "speed_apply" in w:
            w["speed_apply"].configure(command=self.apply_speed_config)
            
        # دکمه + (START): روشن کردن پد
        if "speed_plus" in w:
            w["speed_plus"].configure(command=lambda: self.run_pad_motor(True))
            
        # دکمه - (STOP): خاموش کردن پد
        if "speed_minus" in w:
            w["speed_minus"].configure(command=lambda: self.run_pad_motor(False))

    # ==========================================
    # حلقه اصلی و لاجیک زمانی (Main Loop)
    # ==========================================

    def _start_ui_loop(self):
        try:
            state = self.model.state

            # 1. کرنومتر
            if state.get("stopwatch_running"):
                elapsed = time.time() - state.get("stopwatch_start_time", 0)
                self._update_time_label("stopwatch_label", elapsed)

            # 2. تایمر معکوس
            if state.get("timer_running"):
                rem = state.get("timer_end_target", 0) - time.time()
                
                if rem > 0:
                    state["timer_remaining"] = rem
                    self._update_time_label("timer_total_display", rem)
                else:
                    # زمان تمام شد -> اجرای سناریوی پایان
                    self.finish_sequence()

            self.view.after(100, self._start_ui_loop)
        except Exception as e:
            print(f"UI Loop Error: {e}")

    def _update_time_label(self, widget_key, seconds):
        """تابع کمکی برای نمایش زمان"""
        if seconds < 0: seconds = 0
        if widget_key in self.view.control_widgets:
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            self.view.control_widgets[widget_key].configure(text=f"{h:02}:{m:02}:{s:02}")

    # ==========================================
    # سناریوهای عملیاتی (Operational Logic)
    # ==========================================

    def start_timer_sequence(self):
        """سناریوی شروع: محاسبه زمان + روشن کردن پد + استارت تایمر"""
        total_seconds = (self.timer_setup["h"] * 3600) + \
                        (self.timer_setup["m"] * 60) + self.timer_setup["s"]
        
        if total_seconds == 0:
            self.view.show_info_message("SET TIME FIRST!")
            return

        # [اصلاح شده] خواندن از متغیر Config (سرعت ذخیره شده) نه سرعت لحظه‌ای
        speed = self.model.state.get('config_pad_speed', 0)
        
        if speed == 0:
            self.view.show_info_message("WARNING: SPEED IS 0")
        
        print(f"🚀 SEQUENCE START: Pad ON ({speed}%), Timer {total_seconds}s")
        if hasattr(self.model, "set_dc_speed"):
            self.model.set_dc_speed("pad", speed)

        # استارت تایمر
        self.model.state["timer_end_target"] = time.time() + total_seconds
        self.model.state["timer_remaining"] = total_seconds
        self.model.state["timer_running"] = True

    def finish_sequence(self):
        """سناریوی پایان: توقف پد + عقب‌نشینی ستون"""
        print("🏁 SEQUENCE FINISHED")
        
        # 1. توقف تایمر
        self.model.state["timer_running"] = False
        self.model.state["timer_remaining"] = 0
        self._update_time_label("timer_total_display", 0)
        
        # 2. خاموش کردن موتورها
        if hasattr(self.model, "set_dc_speed"):
            self.model.set_dc_speed("pad", 0)
            self.model.set_dc_speed("lissa", 0)
        
        # 3. عقب‌نشینی خودکار
        print(f"🔙 Auto Retracting {self.RETRACT_DIST_MM} mm...")
        if hasattr(self.model, "move_column_mm"):
            self.model.move_column_mm(self.RETRACT_DIST_MM, "up")
            
        self.view.show_info_message("DONE: MOTORS OFF & RETRACTED")

    def stop_timer(self):
        """توقف دستی تایمر"""
        self.model.state["timer_running"] = False
        # در توقف دستی، معمولاً موتور را هم خاموش می‌کنیم
        if hasattr(self.model, "set_dc_speed"):
            self.model.set_dc_speed("pad", 0)
        print("⏳ Timer Stopped Manually")

    def reset_timer(self):
        self.stop_timer()
        self.model.state["timer_remaining"] = 0
        if "timer_total_display" in self.view.control_widgets:
            self.view.control_widgets["timer_total_display"].configure(text="READY TO START")

    # ==========================================
    # کنترل‌های دستی (Manual Controls)
    # ==========================================

    def move_manual(self, direction):
        """اجرای حرکت دستی ستون (JOG)"""
        try:
            # خواندن مقدار میکرون از پنل
            microns = int(self.view.control_widgets["step"].cget("text"))
            mm = microns / 1000.0
            
            print(f"🕹 Manual Move: {direction} {mm} mm")
            if hasattr(self.model, "move_column_mm"):
                self.model.move_column_mm(mm, direction)
        except Exception as e:
            print(f"Move Error: {e}")

    def run_pad_motor(self, turn_on):
        """کنترل دستی موتور پد با حفظ حافظه سرعت"""
        if turn_on:
            try:
                # اگر در پنل سرعت هستیم، عدد جدید را بخوان و در کانفیگ ذخیره کن
                if "speed" in self.view.control_widgets:
                     val = int(self.view.control_widgets["speed"].cget("text"))
                     self.model.state['config_pad_speed'] = val
                else:
                     # اگر در صفحه دیگری هستیم، از حافظه بخوان
                     val = self.model.state.get('config_pad_speed', 0)
            except: val = 0
            
            print(f"🕹 Manual Pad START: {val}%")
            if hasattr(self.model, "set_dc_speed"):
                self.model.set_dc_speed("pad", val)
        else:
            print("🕹 Manual Pad STOP")
            if hasattr(self.model, "set_dc_speed"):
                # سرعت موتور صفر می‌شود اما کانفیگ دست‌نخورده می‌ماند
                self.model.set_dc_speed("pad", 0)

    def apply_step_config(self):
        try:
            val = int(self.view.control_widgets["step"].cget("text"))
            self.model.state["step_col"] = val
            self.view.show_info_message(f"STEP SAVED: {val}")
        except: pass

    def apply_speed_config(self):
        try:
            val = int(self.view.control_widgets["speed"].cget("text"))
            # [اصلاح شده] ذخیره در متغیر کانفیگ دائمی
            self.model.state["config_pad_speed"] = val
            self.view.show_info_message(f"SPEED SAVED: {val}")
        except: pass

    # ==========================================
    # تنظیمات و کرنومتر (Helpers)
    # ==========================================

    def _adjust_timer_setting(self, unit, delta):
        current = self.timer_setup[unit]
        limit = 23 if unit == "h" else 59
        new_val = current + delta
        if new_val > limit: new_val = 0
        if new_val < 0: new_val = limit
        self.timer_setup[unit] = new_val
        self._refresh_timer_setup_ui()

    def _refresh_timer_setup_ui(self):
        w = self.view.control_widgets
        for unit, val in self.timer_setup.items():
            key = f"timer_{unit}_lbl"
            if key in w:
                w[key].configure(text=f"{val:02}")

    def start_stopwatch(self):
        if not self.model.state.get("stopwatch_running"):
            self.model.state["stopwatch_running"] = True
            elapsed = self.model.state.get("stopwatch_elapsed", 0)
            self.model.state["stopwatch_start_time"] = time.time() - elapsed

    def stop_stopwatch(self):
        if self.model.state.get("stopwatch_running"):
            self.model.state["stopwatch_running"] = False
            self.model.state["stopwatch_elapsed"] = time.time() - self.model.state.get("stopwatch_start_time", 0)

    def reset_stopwatch(self):
        self.model.state["stopwatch_running"] = False
        self.model.state["stopwatch_elapsed"] = 0
        if "stopwatch_label" in self.view.control_widgets:
            self.view.control_widgets["stopwatch_label"].configure(text="00:00:00")

    def handle_save_config(self):
        print("💾 Saving config...")
        self.view.show_info_message("CONFIG SAVED")

    def handle_light_toggle(self):
        current = self.model.state.get("light_intensity", 0)
        target = 0 if current > 0 else 50
        if hasattr(self.model, "set_dc_speed"):
            self.model.set_dc_speed("light", target)
        if "light_scale" in self.view.control_widgets:
            self.view.control_widgets["light_scale"].set(target)

    def handle_light_change(self, value):
        val = int(float(value))
        if hasattr(self.model, "set_dc_speed"):
            self.model.set_dc_speed("light", val)