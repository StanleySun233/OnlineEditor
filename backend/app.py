from flask import Flask, request

import backend
import sql

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
mysqlClient = sql.sqlClient('localhost', '3306', 'oe', 'root', 'root')
mysqlClient.setConnection()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.login(mysqlClient, data)
    return res


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.values.to_dict()
    else:
        data = request.args.to_dict()
    res = backend.register(mysqlClient, data)
    return res


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=False)
