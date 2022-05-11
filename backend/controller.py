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
    res = backend.service.userService.login(mysqlClient, data)
    return res


@app.route('/user/register', methods=['POST', 'GET'])
def userRegister():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.userService.register(mysqlClient, data)
    return res


@app.route('/user/getInfo', methods=['POST', 'GET'])
def userSearch():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.userService.getElemByAccount(mysqlClient, data)
    return res


@app.route('/file/upload', methods=['GET', 'POST'])
def fileUpload():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.fileService.upload(minioClient, mysqlClient, data)
    return res


@app.route('/file/download', methods=['GET', 'POST'])
def fileDownload():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.fileService.download(minioClient, mysqlClient, data)
    return res


@app.route('/file/searchById', methods=['GET', 'POST'])
def fileSearchById():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.fileService.searchById(mysqlClient, data)
    return res


@app.route('/file/searchByUserName', methods=['GET', 'POST'])
def fileSearchByUserName():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.fileService.searchByUserName(mysqlClient, data)
    return res


@app.route('/file/update', methods=['GET', 'POST'])
def fileUpdate():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.service.fileService.update(minioClient, mysqlClient, data)
    return res


def run():
    app.run(host=config.httpIp, port=config.httpPort, debug=False)


if __name__ == "__main__":
    run()
