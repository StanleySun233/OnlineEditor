import config
import tool.mio as mio

minioClient = mio.minioClient(config.minioIp,
                              config.minioPort,
                              config.minioAccount,
                              config.minioPassword,
                              config.minioBucket)
minioClient.setConnection()

minioClient.uploadFile('main', 'py')
