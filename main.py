import threading

import backend.controller
import frontend

app = threading.Thread(target=backend.controller.run)
app.start()

loginWindow = frontend.loginWindow.LoginWindow(400, 300, '登录界面')
