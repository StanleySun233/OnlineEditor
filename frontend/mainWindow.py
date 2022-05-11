import frontend


class MainWindow(frontend.windowWidget.WindowWidget):
    def __init__(self, width, height, name, user_name, user_auth):
        super().__init__(width, height, name)
        self.name = user_name
        self.auth = user_auth
        self.authDict = {0: '用户', 1: '会员', 5: '管理员'}

        self.pictureLabel = self.makeLabel((40, 40, 120, 120), text='设置头像', command=self.pictureLabelPress)
        self.nameLabel = self.makeLabel((180, 40, 120, 40), text=self.name)
        self.authLabel = self.makeLabel((180, 120, 120, 40), text=self.authDict[self.auth])

        self.fileListbox = self.makeListbox((40, 180, 260, 540), self.fileListboxPress)
        self.fileListboxLabel = self.makeLabel((40, 740, 260, 40), '文件栏')

        self.textEditorText = self.makeText((320, 100, 800, 620))
        self.textEditorLabel = self.makeLabel((320, 740, 800, 40), '编辑栏')

        # self.makeButton()

        self.window.mainloop()

    def init(self):
        # TODO
        pass

    def fileListboxPress(self, event):
        # TODO
        pass

    def pictureLabelPress(self, event):
        # TODO
        pass
