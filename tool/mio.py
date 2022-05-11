import io
import os

import minio

import tool


class minioClient:
    def __init__(self, ip, port, account, password, bucket):
        self.ip = ip
        self.port = port
        self.account = account
        self.password = password
        self.url = '{}:{}'.format(self.ip, self.port)
        self.bucket = bucket
        self.connection: minio.Minio = None

    def setConnection(self):
        try:
            conn = minio.Minio(self.url, self.account, self.password, secure=False)
            self.connection = conn
            tool.fun.logFormat(tool.fun.INFO, 'MINIO文件管理系统连接成功')
        except:
            tool.fun.logFormat(tool.fun.WARN, 'MINIO文件管理系统连接失败')
            exit(0)

        try:
            if not self.connection.bucket_exists(self.bucket):
                self.connection.make_bucket(self.bucket)
            else:
                tool.fun.logFormat(tool.fun.INFO, 'MINIO文件管理系统初始化成功')
        except:
            tool.fun.logFormat(tool.fun.WARN, 'MINIO文件管理系统创建桶失败')
            exit(0)

    def uploadFile(self, id, type, file):
        fileName = f'{id}.{type}'
        l = len(file)
        f = io.BytesIO(file)
        self.connection.put_object(self.bucket, fileName, f, l)

    def downloadFile(self, fileName):
        filePath = './{}'.format(fileName)
        if os.path.exists(filePath):
            os.remove(filePath)
        self.connection.fget_object(self.bucket, fileName, filePath)
        file = open(filePath, 'rb')
        f = file.readline()
        file.close()
        if os.path.exists(filePath):
            os.remove(filePath)
        return f
