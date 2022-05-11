import datetime
import io
import json

import minio

import tool


def upload(minioClient: tool.mio.minioClient, mysqlClient: tool.sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}

    sheet = {}
    for i in attrs:
        if i == 'file':
            continue
        else:
            sheet[i] = attrs[i]
    sheet['file_id'] = tool.fun.getTimeStamp()
    sheet['create_date'] = datetime.datetime.now()
    sheet['last_date'] = datetime.datetime.now()
    mysqlClient.insertInfo('file_info', sheet)

    url = minioClient.uploadFile(sheet['file_id'], sheet['file_type'])
    res['data'] = {'url': url, 'file_id': sheet['file_id']}
    res['code'] = 1
    return json.dumps(res)


def download(minioClient: tool.mio.minioClient, mysqlClient: tool.sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}
    data = json.loads(getElemById(mysqlClient, {'file_id': attrs['file_id']}))['data']
    url = minioClient.downloadFile(data['file_id'], data['file_type'])
    res['data'] = {'url': url, 'info': data}
    res['code'] = 1
    return json.dumps(res)


def getElemById(sqlClient: tool.sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}
    data = sqlClient.isExist('file_info', {'file_id': attrs['file_id']})
    if data:
        sheet = sqlClient.searchInfo('file_info', {'file_id': attrs['file_id']})
        dt = {'file_id': sheet[0],
              'file_name': sheet[1],
              'file_type': sheet[2],
              'file_auth': sheet[3],
              'create_date': sheet[4].strftime('%Y-%m-%d %H:%M:%S'),
              'user_name': sheet[5],
              'last_date': sheet[6].strftime('%Y-%m-%d %H:%M:%S')}
        res['data'] = dt
        res['code'] = 1
        res['msg'] = '成功'
    else:
        res['msg'] = '找不到该文件'
    return json.dumps(res)


def searchById(sqlClient: tool.sql.sqlClient, attrs: dict):
    res = getElemById(sqlClient, attrs)
    return json.dumps(res)


def searchByUserName(sqlClient: tool.sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}
    sheet = sqlClient.searchInfo('file_info', {'user_name': attrs['user_name'], 'file_type': attrs['file_type']},
                                 mult=True)
    result = []
    for i in range(len(sheet)):
        dt = {'file_id': sheet[i][0],
              'file_name': sheet[i][1],
              'file_type': sheet[i][2],
              'file_auth': sheet[i][3],
              'create_date': sheet[i][4].strftime('%Y-%m-%d %H:%M:%S'),
              'user_name': sheet[i][5],
              'last_date': sheet[i][6].strftime('%Y-%m-%d %H:%M:%S')}
        result.append(dt)

    res['data'] = result
    res['code'] = 1
    res['msg'] = '成功'

    return json.dumps(res)


def update(minioClient: tool.mio.minioClient, mysqlClient: tool.sql.sqlClient, attrs: dict):
    res = {'code': 0, 'data': None, 'msg': None}
    mysqlClient.update('file_info', {'file_id': attrs['file_id']}, {'last_date': datetime.datetime.now()})
    data = json.loads(getElemById(mysqlClient, attrs))['data']
    url = minioClient.uploadFile(data['file_id'], data['file_type'])
    res['data'] = {'url': url, 'file_id': data['file_id']}
    res['code'] = 1

    return json.dumps(res)
