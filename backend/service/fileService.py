import json

import minio

import tool


def upload(minioClient: tool.mio.minioClient, mysqlClient: tool.sql.sqlClient, attrs: dict):
    f = attrs['file']

    sheet = {}
    for i in attrs:
        if i == 'file':
            continue
        else:
            sheet[i] = attrs[i]

    mysqlClient.insertInfo('file_info', attrs)

    minioClient.uploadFile(sheet['id'], sheet['type'])
