from flask import Flask, request

import backend.service
import config
import tool

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

mysqlClient = tool.sql.sqlClient(config.sqlIp,
                                 config.sqlPort,
                                 config.sqlDatabase,
                                 config.sqlAccount,
                                 config.sqlPassword)

minioClient = tool.mio.minioClient(config.minioIp,
                                   config.minioPort,
                                   config.minioAccount,
                                   config.minioPassword,
                                   config.minioBucket)

mysqlClient.setConnection()
minioClient.setConnection()


@app.route('/user/login', methods=['POST', 'GET'])
def userLogin():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.userInfoService.login(mysqlClient, data)
    return res


@app.route('/user/register', methods=['POST', 'GET'])
def userRegister():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.userInfoService.register(mysqlClient, data)
    return res


@app.route('/userInfo/getInfo', methods=['POST', 'GET'])
def userInfoSearch():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.userInfoService.getInfoByAccount(mysqlClient, data)
    return res


if __name__ == "__main__":
    app.run(host=config.httpIp, port=config.httpPort, debug=False)
