import ttkbootstrap as ttk
import ttkbootstrap.constants as ttk_const


class PolisherView(ttk.Window):
    def __init__(self):
        super().__init__(themename="vapor")
        self.title("Polisher V2")
        self.geometry('800x500')
        self.resizable(False, False)
        self._top_bar()

    def _top_bar(self):
        self.top_frame=ttk.Frame(self, bootstyle=ttk_const.DANGER)
        self.top_frame.pack(side=ttk_const.TOP, fill=ttk_const.X)