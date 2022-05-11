import json
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox

import cv2
import requests

import config
import frontend
import tool.fun


class MainWindow(frontend.windowWidget.WindowWidget):
    def __init__(self, width, height, name, user_name, user_auth):
        super().__init__(width, height, name)
        self.picture = None
        self.data = None
        self.name = user_name
        self.auth = user_auth
        self.authDict = {0: '用户', 1: '会员', 5: '管理员'}
        self.uploadUrl = '{}/{}'.format(config.httpUrl, 'file/upload')
        self.downloadUrl = '{}/{}'.format(config.httpUrl, 'file/download')
        self.searchByIdUrl = '{}/{}'.format(config.httpUrl, 'file/searchById')
        self.searchByUserNameUrl = '{}/{}'.format(config.httpUrl, 'file/searchByUserName')
        self.updateUrl = '{}/{}'.format(config.httpUrl, 'file/update')
        self.ids: str = '1652275980577'

        self.pictureLabel = self.makeLabel((40, 40, 120, 120), '设置头像', command=self.pictureLabelPress)
        self.nameLabel = self.makeLabel((180, 40, 120, 40), self.name)
        self.authLabel = self.makeLabel((180, 120, 120, 40), self.authDict[self.auth])

        self.fileListbox = self.makeListbox((40, 180, 260, 540), self.fileListboxPress)
        self.fileListboxLabel = self.makeLabel((40, 740, 260, 40), '文件栏')

        self.textEditorText = self.makeText((320, 100, 800, 620))
        self.textEditorLabel = self.makeLabel((320, 740, 800, 40), '编辑栏')

        self.uploadButton = self.makeButton((1140, 40, 120, 40), '上传文件', self.uploadButtonPress)
        self.downloadButton = self.makeButton((1280, 40, 120, 40), '下载文件', self.downloadButtonPress)
        self.saveDataButton = self.makeButton((1140, 100, 120, 40), '保存文本', self.saveDataButtonPress)

        self.init()
        self.window.mainloop()

    def init(self):
        # TODO
        data = json.loads(requests.post(self.searchByUserNameUrl,
                                        {'user_name': self.name, 'file_type': 'txt'}).
                          content.decode(encoding='utf-8'))['data']
        self.data = data

        self.fileListbox.delete(0, tk.END)
        self.textEditorText.delete('1.0', tk.END)
        for i in data:
            self.fileListbox.insert(0, '{}!!!{}'.format(i['file_name'], i['file_id']))

        self.fileListbox.activate(0)
        self.picRenew()

        pass

    def fileListboxPress(self, event):
        idx = self.fileListbox.curselection()
        if len(idx):
            idx = idx[0]
        self.ids = self.data[idx]['file_id']
        self.textEditorText.delete('1.0', tk.END)
        self.loadData()
        pass

    def pictureLabelPress(self, event):
        # TODO
        path = tk.filedialog.askopenfilename()
        name = os.path.basename(path)
        file_name = os.path.splitext(name)[0]
        file_type = os.path.splitext(name)[1][1:]

        img = cv2.imread(path)
        img = cv2.resize(img, (120, 120))
        cv2.imwrite('./temp.png', img)
        f = open('./temp.png', 'rb')
        file = f.read()
        f.close()
        os.remove('./temp.png')
        file_auth = self.auth
        user_name = self.name
        data = {'file_name': file_name, 'file_type': file_type, 'file_auth': file_auth,
                'user_name': user_name}
        url = json.loads(requests.post(self.uploadUrl, data=data).content.decode('utf-8'))['data']['url']
        res = requests.put(url, file)
        if int(res.status_code) == 200:
            tk.messagebox.showinfo('上传', '文件上传成功')
            self.init()
        else:
            tk.messagebox.showwarning('上传', '文件上传失败')
        pass
        pass

    def uploadButtonPress(self, *args):
        path = tk.filedialog.askopenfilename()
        name = os.path.basename(path)
        f = open(path, 'rb')
        file = f.read()
        f.close()
        file_name = os.path.splitext(name)[0]
        file_type = os.path.splitext(name)[1][1:]
        file_auth = self.auth
        user_name = self.name
        data = {'file_name': file_name, 'file_type': file_type, 'file_auth': file_auth,
                'user_name': user_name}
        url = json.loads(requests.post(self.uploadUrl, data=data).content.decode('utf-8'))['data']['url']
        res = requests.put(url, file)
        if int(res.status_code) == 200:
            tk.messagebox.showinfo('上传', '文件上传成功')
            self.init()
        else:
            tk.messagebox.showwarning('上传', '文件上传失败')
        pass

    def downloadButtonPress(self, *args):
        data = json.loads(requests.post(self.downloadUrl, {'file_id': self.ids}).text)['data']
        url = data['url']
        data = data['info']
        path = tk.filedialog.asksaveasfilename(initialfile='{}.{}'.format(data['file_name'], data['file_type']),
                                               filetypes=[('文件', '.{}'.format(data['file_type']))])
        file = requests.get(url).content
        with open(path, 'wb') as f:
            f.write(file)
        tk.messagebox.showinfo('下载', '文件下载成功')
        pass

    def loadData(self, *args):
        data = json.loads(requests.post(self.downloadUrl, {'file_id': self.ids}).text)['data']
        url = data['url']
        file = requests.get(url).content.decode('utf-8')
        self.textEditorText.insert('end', file)
        pass

    def saveDataButtonPress(self, *args):
        data = self.textEditorText.get('0.0', tk.END)
        f = bytes(data, encoding='utf-8')
        url = json.loads(requests.post(self.updateUrl,
                                       data={'file_id': self.ids, 'file_type': 'txt'}).
                         content.decode(encoding='utf-8'))['data']['url']

        res = requests.put(url, f)
        if int(res.status_code) == 200:
            tk.messagebox.showinfo('上传', '文件上传成功')
            self.init()
        else:
            tk.messagebox.showwarning('上传', '文件上传失败')
        pass

    def picRenew(self):
        picName = json.loads(requests.post(self.searchByUserNameUrl,
                                           {'user_name': self.name, 'file_type': 'png'}).
                             content.decode(encoding='utf-8'))['data']
        picId = picName[-1]['file_id']
        data = json.loads(requests.post(self.downloadUrl, {'file_id': picId}).text)['data']
        url = data['url']
        file = requests.get(url).content
        with open('{}.png'.format(picId), 'wb') as f:
            f.write(file)

        self.picture = tool.fun.pic2TKpic('{}.png'.format(picId), (120, 120))
        self.pictureLabel.configure(image=self.picture)

        os.remove('{}.png'.format(picId))
