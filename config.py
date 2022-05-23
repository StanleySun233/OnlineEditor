httpIp = '127.0.0.1'
httpPort = '5000'
httpUrl = 'http://{}:{}'.format(httpIp, httpPort)

sqlIp = 'localhost'
sqlPort = '3306'
sqlAccount = 'root'
sqlPassword = 'root'
sqlDatabase = 'oe'

# minioIp = '47.100.93.63'
# minioPort = '9090'
# minioAccount = 'admin'
# minioPassword = 'admin123456'
# minioBucket = 'editor'

minioIp = 'localhost'
minioPort = '9000'
minioAccount = 'minioadmin'
minioPassword = 'minioadmin'
minioBucket = 'editor'

userLoginUrl = '{}/{}'.format(httpUrl, 'user/login')
userRegisterUrl = '{}/{}'.format(httpUrl, 'user/register')
userForgetUrl = '{}/{}'.format(httpUrl, 'user/forget')
