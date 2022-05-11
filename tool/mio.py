import minio
import tool.fun as fun


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
            fun.logFormat(fun.INFO, 'MINIO文件管理系统连接成功')
        except:
            fun.logFormat(fun.WARN, 'MINIO文件管理系统连接失败')
            exit(0)
