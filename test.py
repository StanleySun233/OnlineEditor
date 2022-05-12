import requests

res = requests.post('http://127.0.0.1:5000/file/searchByUserName',
                    {'user_name': '1'})
print(res.text)

# minioClient = tool.mio.minioClient(config.minioIp,
#                                    config.minioPort,
#                                    config.minioAccount,
#                                    config.minioPassword,
#                                    config.minioBucket)
#
# minioClient.setConnection()
#
# res = minioClient.downloadFile('1652270302830', 'py')
# f = open('res.py','bw')
# f.write(res)
# f.close()
