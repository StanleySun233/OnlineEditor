import datetime
import json
import urllib.parse

import requests

import config
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
    if 'file_type' in [i for i in attrs.keys()]:
        sheet = sqlClient.searchInfo('file_info', {'user_name': attrs['user_name'], 'file_type': attrs['file_type']},
                                     mult=True)
    else:
        sheet = sqlClient.searchInfo('file_info', {'user_name': attrs['user_name']},
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


def delete(mysqlClient: tool.sql.sqlClient, attrs: dict):
    res = {'code': 1, 'data': None, 'msg': None}
    sheet = mysqlClient.searchInfo('file_info', {'file_id': attrs['file_id']})
    dt = {'file_id': sheet[0],
          'file_name': sheet[1],
          'file_type': sheet[2],
          'file_auth': sheet[3],
          'create_date': sheet[4].strftime('%Y-%m-%d %H:%M:%S'),
          'user_name': sheet[5],
          'last_date': sheet[6].strftime('%Y-%m-%d %H:%M:%S'),
          'del_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    mysqlClient.delInfo('file_info', {'file_id': attrs['file_id']})
    mysqlClient.insertInfo('file_info_del', dt)
    res['msg'] = '删除成功'
    res['data'] = dt

    return json.dumps(res)


def share(minioClient: tool.mio.minioClient, mysqlClient: tool.sql.sqlClient, attrs: dict):
    usr = mysqlClient.searchInfo('user_info', {'user_account': attrs['user_account']})
    sheet = mysqlClient.searchInfo('file_info', {'file_id': attrs['file_id']})

    dt = {'file_id': tool.fun.getTimeStamp(),
          'file_name': sheet[1],
          'file_type': sheet[2],
          'file_auth': sheet[3],
          'create_date': sheet[4].strftime('%Y-%m-%d %H:%M:%S'),
          'user_name': usr[1],
          'last_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    url = minioClient.uploadFile(dt['file_id'], dt['file_type'])
    mysqlClient.insertInfo('file_info', dt)

    mysqlClient.insertInfo('file_share',
                           {'file_id': attrs['file_id'], 'file_to': attrs['user_account'], 'file_from': sheet[5]
                               , 'file_new': dt['file_id'], 'share_date': dt['last_date']})

    return json.dumps({'code': 1, 'data': {'url': url, 'info': dt}, 'msg': '分享成功'})


def online(minioClient: tool.mio.minioClient, attrs: dict):
    key = [i for i in attrs.keys()]
    showType = ['txt', 'md', 'html', 'sql']
    picType = ['png', 'jpg', 'jpeg']
    if 'id' in key:
        url = minioClient.downloadFile(attrs['id'], attrs['type'])
        if attrs['type'] in picType:
            f = open('backend/service/sample/online.html', 'r', encoding='utf-8')
            ht = f.read()
            f.close()
            ht = ht.format('图片查看器', "<img src=\"{}\"".format(url))
            return ht
        elif attrs['type'] not in showType:
            f = open('backend/service/sample/online.html', 'r', encoding='utf-8')
            ht = f.read()
            f.close()
            ht = ht.format('下载链接', "<div><a href=\"{}\">文件下载</a></div>".format(url))
            return ht
        elif attrs['type'] == 'md':
            f = open('backend/service/sample/online.html', 'r', encoding='utf-8')
            ht = f.read()
            f.close()

            text = requests.get(url).content.decode(encoding='utf-8').split('\n')
            t = []
            for i in text:
                print(i)
                if i[0:2] == '# ':
                    t.append(f'<p><h1>{i[2:]}<h1></p>')
                elif i[0:3] == '## ':
                    t.append(f'<p><h2>{i[3:]}<h2></p>')
                elif i[0:4] == '### ':
                    t.append(f'<p><h3>{i[4:]}<h3></p>')
                elif len(i) == 0:
                    t.append('<p></p>')
                elif i[0] == '$' and i[-1] == '$':
                    s = urllib.parse.quote(i[1:-1])
                    u = '<img src="https://www.zhihu.com/equation?tex={}">'.format(s)
                    t.append(f'<p>{u}</p>')
                elif i[0] == '_' and i[-1] == '_':
                    t.append(f'<p><i>{i[1:-1]}</i></p>')
                elif i[0:2] == '**' and i[-2] + i[-1] == '**':
                    t.append(f'<p><b>{i[2:-2]}</b></p>')
                else:
                    t.append('<p>{}</p>'.format(i))
            t.append("<div><a href=\"{}\">文件下载</a></div>".format(url))
            ts = ''
            for i in t:
                ts += i
            ht = ht.format('文本读取器', ts)
            return ht
        else:
            f = open('backend/service/sample/online.html', 'r', encoding='utf-8')
            ht = f.read()
            f.close()

            text = requests.get(url).content.decode(encoding='utf-8').split('\n')
            t = ['<p>{}</p>\n'.format(i) for i in text]
            ts = ''
            for i in t:
                ts += i
            ht = ht.format('文本读取器', ts)
            return ht
    elif 'file_id' in key:
        return json.dumps(
            {'msg': '分享成功',
             'data': {
                 'url': '{}/file/online?id={}&type={}'.format(config.httpUrl, attrs['file_id'], attrs['file_type'])}})
