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
        self.showType = ['txt', 'md', 'html', 'sql', 'csv']
        self.type = None
        self.picture = None
        self.data = None
        self.v1 = tk.StringVar()
        self.name = user_name
        self.auth = user_auth
        self.authDict = {0: '用户', 1: '会员', 5: '管理员'}
        self.uploadUrl = '{}/{}'.format(config.httpUrl, 'file/upload')
        self.downloadUrl = '{}/{}'.format(config.httpUrl, 'file/download')
        self.searchByIdUrl = '{}/{}'.format(config.httpUrl, 'file/searchById')
        self.searchByUserNameUrl = '{}/{}'.format(config.httpUrl, 'file/searchByUserName')
        self.updateUrl = '{}/{}'.format(config.httpUrl, 'file/update')
        self.deleteUrl = '{}/{}'.format(config.httpUrl, 'file/delete')
        self.shareUrl = '{}/{}'.format(config.httpUrl, 'file/share')
        self.onlineUrl = '{}/{}'.format(config.httpUrl, 'file/online')
        self.ids: str = '1652275980577'

        self.pictureLabel = self.makeLabel((40, 40, 120, 120), '设置头像', command=self.pictureLabelPress)
        self.nameLabel = self.makeLabel((180, 40, 120, 40), self.name)
        self.authLabel = self.makeLabel((180, 120, 120, 40), self.authDict[self.auth])

        self.fileListbox = self.makeListbox((40, 180, 260, 540), self.fileListboxPress)
        self.fileListboxLabel = self.makeLabel((40, 740, 260, 40), '文件栏')

        self.textEditorFileId = self.makeLabel((320, 40, 800, 40))

        self.textBButton = self.makeButton((320, 100, 40, 40), 'B', self.textBButtonPress)

        self.textIButton = self.makeButton((360, 100, 40, 40), 'I', self.textIButtonPress)

        self.text1Button = self.makeButton((400, 100, 40, 40), '1', self.text1ButtonPress)
        self.text2Button = self.makeButton((440, 100, 40, 40), '2', self.text2ButtonPress)
        self.text3Button = self.makeButton((480, 100, 40, 40), '3', self.text3ButtonPress)
        self.textTButton = self.makeButton((520, 100, 40, 40), 'T', self.textTButtonPress)
        self.textSButton = self.makeButton((520, 100, 40, 40), '$', self.textSButtonPress)

        self.textEditorText = self.makeText((320, 180, 820, 520))
        self.textEditorLabel = self.makeLabel((320, 740, 800, 40), '编辑栏')

        self.uploadButton = self.makeButton((1140, 40, 120, 40), '上传文件', self.uploadButtonPress)
        self.downloadButton = self.makeButton((1280, 40, 120, 40), '下载文件', self.downloadButtonPress)
        self.saveDataButton = self.makeButton((1140, 100, 120, 40), '保存文件', self.saveDataButtonPress)
        self.deleteDataButton = self.makeButton((1280, 100, 120, 40), '删除文件', self.deleteDataButtonPress)

        self.shareFileButton = self.makeButton((1140, 160, 120, 40), '共享文件', self.shareFileButtonPress)
        self.onlineFileButton = self.makeButton((1280, 160, 120, 40), '分享文件', self.onlineFileButtonPress)

        self.shareFileEntry = self.makeEntry((1140, 220, 260, 40))

        self.init()
        self.window.mainloop()

    def init(self):
        data = json.loads(requests.post(self.searchByUserNameUrl,
                                        {'user_name': self.name}).
                          content.decode(encoding='utf-8'))['data']
        self.data = data
        self.fileListbox.delete(0, tk.END)
        self.textEditorText.delete('1.0', tk.END)
        for i in data:
            self.fileListbox.insert(0,
                                    '{}.{}@{}@{}'.format(i['file_name'], i['file_type'], i['file_id'], i['user_name']))
        self.data.reverse()

        self.fileListbox.activate(0)
        self.picRenew()

        pass

    def fileListboxPress(self, event):
        idx = self.fileListbox.curselection()
        if len(idx):
            idx = idx[0]
        self.ids = self.data[idx]['file_id']
        self.type = self.data[idx]['file_type']
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorFileId.configure(text=str(self.ids))
        if self.type not in self.showType:
            self.textEditorText.insert('end', '非二进制文本文件无法查看，但是可以共享和分享。')
            return
        self.loadData()
        pass

    def pictureLabelPress(self, event):
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
        data = {'file_name': file_name, 'file_type': 'png', 'file_auth': file_auth,
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
        if self.type not in ['txt', 'md', 'html']:
            tk.messagebox.showwarning('保存', '非二进制格式的文件无法保存')
            return
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

    def deleteDataButtonPress(self, *args):
        res = json.loads(requests.post(self.deleteUrl, data={'file_id': self.ids}).content.decode('utf-8'))
        if int(res['code']) == 1:
            tk.messagebox.showinfo('删除', res['msg'])
        else:
            tk.messagebox.showwarning('删除', '删除失败')
        self.init()
        pass

    def shareFileButtonPress(self, *args):
        name = self.shareFileEntry.get()
        res = json.loads(
            requests.post(self.shareUrl, data={'file_id': self.ids, 'user_account': name}).content.decode('utf-8'))
        url = res['data']['url']
        data = self.textEditorText.get('0.0', tk.END)
        f = bytes(data, encoding='utf-8')
        res = requests.put(url, f)
        if int(res.status_code) == 200:
            tk.messagebox.showinfo('上传', '文件共享成功')
            self.init()
        else:
            tk.messagebox.showwarning('上传', '文件共享失败')
        pass

    def onlineFileButtonPress(self, *args):
        res = json.loads(
            requests.post(self.onlineUrl, {'file_id': self.ids, 'file_type': self.type}).content.decode('utf-8'))
        self.shareFileEntry.configure(textvariable=self.v1)
        self.v1.set('')
        self.shareFileEntry.insert(0, res['data']['url'])
        tk.messagebox.showinfo('分享', '文件分享成功')
        pass

    def textBButtonPress(self, *args):
        rep = self.textEditorText.selection_get().replace('**', '')
        data = self.textEditorText.get('0.0', tk.END)
        if '**{}**'.format(rep) in data:
            data = data.replace('**{}**'.format(rep), rep)
        else:
            data = data.replace(rep, '**{}**'.format(rep))
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorText.insert('end', data[:-1])
        pass

    def textIButtonPress(self, *args):
        rep = self.textEditorText.selection_get().replace('_', '')
        data = self.textEditorText.get('0.0', tk.END)
        if '_{}_'.format(rep) in data:
            data = data.replace('_{}_'.format(rep), rep)
        else:
            data = data.replace(rep, '_{}_'.format(rep))
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorText.insert('end', data[:-1])
        pass

    def text1ButtonPress(self, *args):
        rep = self.textEditorText.selection_get()
        data = self.textEditorText.get('0.0', tk.END)
        if "# " == rep[:2]:
            data = data.replace(rep, rep[2:])
        else:
            data = data.replace(rep, '# {}'.format(rep))
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorText.insert('end', data[:-1])
        pass

    def text2ButtonPress(self, *args):
        rep = self.textEditorText.selection_get()
        data = self.textEditorText.get('0.0', tk.END)
        if "## " == rep[:3]:
            data = data.replace(rep, rep[3:])
        else:
            data = data.replace(rep, '## {}'.format(rep))
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorText.insert('end', data[:-1])
        pass

    def text3ButtonPress(self, *args):
        rep = self.textEditorText.selection_get()
        data = self.textEditorText.get('0.0', tk.END)
        if "### " == rep[:4]:
            data = data.replace(rep, rep[4:])
        else:
            data = data.replace(rep, '### {}'.format(rep))
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorText.insert('end', data[:-1])
        pass

    def textTButtonPress(self, *args):
        rep = self.textEditorText.selection_get()
        data = self.textEditorText.get('0.0', tk.END)
        if "# " == rep[:2]:
            data = data.replace(rep, rep[2:])
        elif "## " == rep[:3]:
            data = data.replace(rep, rep[3:])
        elif "### " == rep[:4]:
            data = data.replace(rep, rep[4:])
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorText.insert('end', data[:-1])
        pass

    def textSButtonPress(self, *args):
        rep = self.textEditorText.selection_get().replace('$', '')
        data = self.textEditorText.get('0.0', tk.END)
        if '${}$'.format(rep) in data:
            data = data.replace('${}$'.format(rep), rep)
        else:
            data = data.replace(rep, '${}$'.format(rep))
        self.textEditorText.delete('1.0', tk.END)
        self.textEditorText.insert('end', data[:-1])
        pass
