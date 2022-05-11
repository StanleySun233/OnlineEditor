from flask import Flask, request

import config
from tool import sql
import backend.service as service

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
mysqlClient = sql.sqlClient('localhost', '3306', 'oe', 'root', 'root')
mysqlClient.setConnection()


@app.route('/user/login', methods=['POST', 'GET'])
def userLogin():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = service.userInfoService.login(mysqlClient, data)
    return res


@app.route('/user/register', methods=['POST', 'GET'])
def userRegister():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = service.userInfoService.register(mysqlClient, data)
    return res


@app.route('/userInfo/getInfo', methods=['POST', 'GET'])
def userInfoSearch():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = service.userInfoService.getInfoByAccount(mysqlClient, data)
    return res


if __name__ == "__main__":
    app.run(host=config.httpIp, port=config.httpPort, debug=False)
