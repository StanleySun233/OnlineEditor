# OnlineEditor

关键词：前后端分离、Flask、数据库、Tkinter、课程设计 在线文档共享编辑系统

# 0. 需求

1. python

使用Anaconda作为环境管理器。 python版本为3.7。

```shell
pip install minio 
pip install flask
pip install opencv-python
pip install pymysql
pip install requests
pip install pillow
pip install matplotlib
```

2. Minio

使用docker配置。

```shell
docker search minio
docker pull minio/minio

docker run -d -p 9000:9000 -p 9090:9090 --name=minio --restart=always -e "MINIO_ROOT_USER=admin" -e "MINIO_ROOT_PASSWORD=admin123456" -v /home/data:/data -v /home/config:/root/.minio  minio/minio server /data --console-address ":9000" --address ":9090"
```

3. MySql

版本为8.0

# 1. 运行

测试时，可以直接运行main.py。

用作前后端分离，后端机运行backend/controller.py，前端机运行tk.py。

# 2. 文档

开发完成后编写文档

# 3. 报告

开发完成后编写报告