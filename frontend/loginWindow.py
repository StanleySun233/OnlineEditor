import hashlib
import json
import tkinter.messagebox

import requests

import config
import frontend.windowWidget


class LoginWindow(frontend.windowWidget.WindowWidget):
    def __init__(self, width, height, name):
        super().__init__(width, height, name)
        self.loginUrl = '{}/{}'.format(config.httpUrl, 'user/login')
        self.registerUrl = '{}/{}'.format(config.httpUrl, 'user/register')

        self.accountLabel = self.makeLabel((20, 40, 100, 40), '账号：')
        self.passwordLabel = self.makeLabel((20, 120, 100, 40), '密码：')

        self.accountEntry = self.makeEntry((140, 40, 240, 40))
        self.passwordEntry = self.makeEntry((140, 120, 240, 40))

        self.loginButton = self.makeButton((80, 220, 100, 40), '登录', self.loginButtonPress)
        self.registerButton = self.makeButton((220, 220, 100, 40), '注册', self.registerButtonPress)

        self.window.mainloop()

    def loginButtonPress(self, *args):
        res = json.loads(requests.post(self.loginUrl, data=self.getAccountAndPassword()).text)
        if res['code'] == 1:
            tkinter.messagebox.showinfo('登录', res['msg'])
            name = self.accountEntry.get()
            self.window.destroy()
            MainWindow = frontend.mainWindow.MainWindow(1440, 800, '在线文档编辑系统', name, res['data']['auth'])
        else:
            tkinter.messagebox.showwarning('登录', res['msg'])

    def registerButtonPress(self, *args):
        res = json.loads(requests.post(self.registerUrl, data=self.getAccountAndPassword()).text)
        if res['code'] == 1:
            tkinter.messagebox.showinfo('注册', res['msg'])
        else:
            tkinter.messagebox.showwarning('注册', res['msg'])
        pass

    def getAccountAndPassword(self):
        return {'account': self.accountEntry.get(),
                'password': hashlib.sha256(self.passwordEntry.get().encode('utf-8')).hexdigest()}
