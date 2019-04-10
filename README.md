# Genethesis

Genethesis是一个用来卡片式撰写论文，并自动生成docx文档的应用。在Alpha测试中支持中文和西班牙语的双语论文。

## 组成

本应用由用户系统和论文生成两部分组成。用户系统用 [Python-Flask](http://flask.pocoo.org) 编写，负责收集用户信息和论文内容，论文生成部分用 [Node.js](https://nodejs.org) 以及 [Docx.js](https://docx.js.org) 编写，负责根据数据库中的论文信息渲染docx文档。文件目录如下：
```bash
Genethesis # 主目录
---- Genethesis # 用户系统
---- Genethesis-docx # 论文生成部分
---- run.py # 主程序入口
---- dependencies.txt # Python依赖包列表
```

## 本地运行

首先请确保本地安装有Node.js 10+以及Python 3.7+。下载或克隆该项目后，终端进入本项目主目录，安装Python依赖包：
```bash
python3 -m venv venv # 创建新虚拟环境
source venv/bin/activate # 激活虚拟环境
pip install -r dependencies.txt # 安装依赖包
# 在Ubuntu系统下，有可能需要提前安装wheel等依赖库
```
在虚拟环境下输入 python 进入Python终端，初始化数据库：
```python
from Genethesis import db
db.create_all()
exit()
```
本地运行用户系统程序：
```bash
python run.py
# 保持该终端窗口开启，否则程序将关闭
```
新建终端窗口并进入本项目主目录，安装Node.js依赖包：
```bash
cd Genethesis-docx && npm install
```
安装完成后，本地运行论文生成程序：
```bash
npm start
# 保持该终端窗口开启，否则程序将关闭
```
此时即可访问 localhost:5000 打开本系统。

## 注意事项

论文生成系统默认运行在 3000 端口，如果该端口被占用，需要修改，请在 Genethesis-docx/app.js 末尾处更改，同时请前往 Genethesis/articles/routes.py 搜索 localhost:3000 并替换端口数，应有两处。

## 其他声明

这是一个业余人士闲着无聊做来玩的项目，请不要抱以以太高的期待。此外，该项目完全免费开源，该业余人士随时可能停止更新。