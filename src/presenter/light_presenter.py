class LightPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.slider = self.view.control_widgets["light_scale"]
        self.toggle = self.view.control_widgets['light_toggle']

        self.slider.configure(command=self.on_slider_change)
        self.toggle.configure(command=self.on_toggle)

    
    def on_slider_change(self, value):
        if 'selected' in self.toggle.state():
            brightness = int(float(value))
            self.model.set_brightness(brightness)

    def on_toggle(self):
        if 'selected' in self.toggle.state():
            current_brightness = int(self.slider.get())
            self.model.set_brightness(current_brightness)
        else:
            self.model.set_brightness(0)