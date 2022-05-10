import requests

a = requests.post('http://localhost:5000/register', data={'account': 'test123', 'password': '12345'})
print(a.content.decode(encoding='utf-8'))

# import sql
#
# mysqlClient = sql.sqlClient('localhost', '3306', 'oe', 'root', 'root')
# mysqlClient.setConnection()
# mysqlClient.insertInfo('user_info', {'user_account': 'hello', 'user_password': '12345', 'user_auth': 0})
