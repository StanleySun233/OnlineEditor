import pymysql

import tool


class sqlClient:
    def __init__(self, host, port, dataBase, user, password):
        self.connection = None
        self.host = host
        self.port = int(port)
        self.db = dataBase
        self.user = user
        self.password = password
        self.connection: pymysql.connect

    def setConnection(self):
        try:
            self.connection = pymysql.connect(host=self.host,
                                              port=self.port,
                                              db=self.db,
                                              user=self.user,
                                              password=self.password)
            tool.fun.logFormat(tool.fun.INFO, '成功连接数据库')
        except:
            tool.fun.logFormat(tool.fun.WARN, '数据库连接失败')
            exit(0)

    def insertInfo(self, table, args):
        cur = self.connection.cursor()
        if type(args) == list:
            value = ''
            for i in args:
                value += ("\'{}\',".format(str(i)))
            value = '({})'.format(value[:-1])
            sqlString = 'insert into {} values {}'.format(table, value)
        else:
            att = ''
            for i in args.keys():
                att += '{} ,'.format(i)
            att = '({})'.format(att[:-1])

            value = ''
            for i in args.keys():
                value += '\'{}\','.format(args[i])
            value = '({})'.format(value[:-1])
            sqlString = 'insert into {}{} values {}'.format(table, att, value)
        cur.execute(sqlString)
        self.connection.commit()
        tool.fun.logFormat(tool.fun.INFO, "在表 {} 插入数据 {}".format(table, value))

    def delInfo(self, table, ids):
        value = 'delete from {} where id = {}'.format(table, ids)
        cur = self.connection.cursor()
        cur.execute(value)
        self.connection.commit()
        tool.fun.logFormat(tool.fun.INFO, "在表 {} 刪除数据 {}".format(table, ids))

    def searchInfo(self, table, attrs=None, val=None, mult=False):
        if attrs is None:
            attrs = ''
        if val is None:
            val = []
        sel = ''
        for i in val:
            sel += '{},'.format(i)
        sel = '({})'.format(sel[:-1])
        if len(attrs) == 0:
            value = 'select {} from {}'.format(sel, table)
        else:
            value = ''
            for i in attrs:
                value += ('{} = \'{}\' and'.format(i, attrs[i]))
            value = 'select {} from {} where {}'.format(sel, table, value[:-4])
        cur = self.connection.cursor()
        cur.execute(value)
        res = cur.fetchall()
        if not mult:
            res = res[0]
        tool.fun.logFormat(tool.fun.INFO, '在表 {} 查找数据 {}'.format(table, attrs))
        return res

    def isExist(self, table, attrs=None):
        if attrs is None:
            attrs = ''
        if len(attrs) == 0:
            value = 'select * from {}'.format(table)
        else:
            value = ''
            for i in attrs:
                value += ('{} = \'{}\' and '.format(i, attrs[i]))
            value = 'select * from {} where {}'.format(table, value[:-4])
        cur = self.connection.cursor()
        cur.execute(value)
        res = cur.fetchall()
        tool.fun.logFormat(tool.fun.INFO, '在表 {} 查找数据 {}'.format(table, attrs))
        if len(res) > 0:
            return True
        else:
            return False
