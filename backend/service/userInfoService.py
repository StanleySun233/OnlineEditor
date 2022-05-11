import json

import tool.fun as fun
import tool.sql as sql


def login(sqlClient: sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}
    if 'account' not in attrs.keys():
        res['msg'] = '请求参数没有账号'
        return res
    if 'password' not in attrs.keys():
        res['msg'] = '请求参数没有密码'
        return res
    account = attrs['account']
    password = attrs['password']
    data = sqlClient.isExist('user_info', {'user_account': account, 'user_password': password})
    if data:
        auth = sqlClient.searchInfo('user_info', {'user_account': account}, val=['user_auth'])[0]
        res['data'] = {'auth': int(auth)}
        res['msg'] = '登录成功'
        res['code'] = 1
    else:
        res['msg'] = '账号或密码不存在'
    return json.dumps(res, ensure_ascii=False)


def register(sqlClient: sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}

    if 'account' not in attrs.keys():
        res['msg'] = '请求参数没有账号'
        return res

    if 'password' not in attrs.keys():
        res['msg'] = '请求参数没有密码'
        return res

    account = attrs['account']
    password = attrs['password']

    data = sqlClient.isExist('user_info', {'user_account': account})

    if data:
        res['msg'] = '账号已存在'
    else:
        sqlClient.insertInfo('user_info',
                             {'user_id': fun.getTimeStamp(), 'user_account': account, 'user_password': password})
        res['msg'] = '注册成功'
        res['code'] = 1
        res['data'] = {'auth': 0}
    return json.dumps(res, ensure_ascii=False)


def getInfoByAccount(sqlClient: sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}
    data = sqlClient.isExist('user_info', {'user_account': attrs['account']})
    if data:
        sheet = sqlClient.searchInfo('user_info', {'user_account': attrs['account']})
        res['data'] = [i for i in sheet]
        res['code'] = 1
        res['msg'] = '成功'
    else:
        res['msg'] = '找不到该用户'
    return res
