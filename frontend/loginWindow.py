from windowWidget import *


class LoginWindow(WindowWidget):
    def __init__(self, width, height, name):
        super().__init__(width, height, name)
        self.window.mainloop()
