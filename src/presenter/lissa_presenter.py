class LissaPresenter:
    def __init__(self, view, model):
        self.model = model
        self.view = view

        self.toggle = view.control_widgets['lissa_toggle']
        self.toggle.configure(command = self.on_toggle_lissa)

    def on_toggle_lissa(self):
        is_on = 'selected' in self.toggle.state()
        self.model.set_state(is_on)
        