from setuptools import setup, find_packages

PACKAGE = "SynicDomain"
NAME = "SynicDomain"
DESCRIPTION = "A async Domain-Drive-Desgin support API develop framework,一个异步的，支持领域驱动开发的应用程序接口开放框架。"
AUTHOR = "Taylor"
AUTHOR_EMAIL = "tank357@icloud.com"
URL = "https://github.com/TaylorHere/SynicDomain"
VERSION = "0.0.6.1"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description="""
    # SynicDomain

A async Domain-Drive-Desgin support API develop framework

一个异步的，支持领域驱动开发的应用程序接口开放框架。

------

## 安装与实例

本框架支持Python3.6及以上版本的，目前只支持git clone

~~~shell
git clone https://github.com/TaylorHere/SynicDomain.git
#查看实例
cd SynicDomain
python3.6 main.py
~~~

------

## 简单实例

~~~python
from SynicDomain import SynicDomain, Handler, Middware, Async_Task, SQLalchemyView
#导入相关模块

app = SynicDomain()
#初始化一个SynicDomain App

@app.url('/', ['after_handle', 'login', 'before_handle', 'create_log'])
#将下面的类与url '/' 进行绑定，并且当用户访问这个url的时候
#按照after_handle、login、before_handle、create_log这样的顺序
#启动自己或其他endpoint
@app.endpoint
#声明下面的类是一个endpoint，endpoint可以与url进行绑定
class login(Handler):
    #一个处理登陆事务的类，其父类为Handler
    async def core(self, cross_line, request):
    #一个异步方法叫做core，其参数cross_line是一个信息结构体
    #参数request是当次访问的请求对象
        name = request.header('name')
        #获取head
        cross_line.add_result(self, name)
        #给结构体添加一些信息
        return str(cross_line)
        #将结构体字符画并返回

if __name__ == '__main__':
    app.run()
    #启动服务
~~~


    """,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="GPL",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=False,
    install_requires=['SQLAlchemy', 'httptools', 'uvloop', 'aiofiles'],
    entry_points={
        # 'console_scripts': [
        #     'sample=sample:main',
        # ],
    },
)
