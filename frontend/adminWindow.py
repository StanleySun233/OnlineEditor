import json
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

import pandas as pd
import requests

import config
import frontend.windowWidget


class AdminWindow(frontend.windowWidget.WindowWidget):
    def __init__(self, width, height, name):
        super().__init__(width, height, name)

        self.userInfoUrl = '{}/{}'.format(config.httpUrl, 'admin/userInfo')
        self.userFileInfoUrl = '{}/{}'.format(config.httpUrl, 'admin/userFileInfo')
        self.userDeleteUrl = '{}/{}'.format(config.httpUrl, 'file/delete')

        self.userInfoButton = self.makeButton((20, 20, 100, 40), '查询用户信息', self.userInfoButtonPress)
        self.userInfoEntry = self.makeEntry((140, 20, 200, 40))

        self.userFileInfoButton = self.makeButton((20, 80, 100, 40), '查询用户文件', self.userFileInfoButtonPress)
        self.userFileInfoEntry = self.makeEntry((140, 80, 200, 40))

        self.userFileDelButton = self.makeButton((20, 140, 100, 40), '删除用户文件', self.userFileDelButtonPress)
        self.userFileDelEntry = self.makeEntry((140, 140, 200, 40))

        self.window.mainloop()

    def userInfoButtonPress(self, *args):
        res = json.loads(requests.post(self.userInfoUrl, data={'user_account': self.userInfoEntry.get()}).text)['data']
        data = '用户id：{}\n用户名：{}\n用户加密密码：{}'.format(res['user_id'], res['user_account'], res['user_password'])

        tk.messagebox.showinfo('用户信息', data)

    def userFileInfoButtonPress(self, *args):
        path = tk.filedialog.askdirectory()
        res = json.loads(requests.post(self.userFileInfoUrl, data={'user_account': self.userFileInfoEntry.get()}).text)[
            'data']

        df = pd.DataFrame(res)
        df.to_csv('{}/{}.csv'.format(path, self.userFileInfoEntry.get()), index=False, encoding='utf-8')

        os.system('start {}/{}.csv'.format(path, self.userFileInfoEntry.get()))

    def userFileDelButtonPress(self, *args):
        ids = self.userFileDelEntry.get()
        print(ids)
        res = json.loads(requests.post(self.userDeleteUrl, data={'file_id': ids}).content)['data']
        tk.messagebox.showinfo('删除', '删除成功')
