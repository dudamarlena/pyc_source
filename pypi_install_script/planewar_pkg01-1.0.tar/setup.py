#引入构建包信息的模块
from distutils.core import setup

#定义发布的包文件的信息

setup(
    name = 'planewar_pkg01', #发布的包文件名称
    version = '1.0',  #发布的包的版本序号
    description = '我的测试包', #发布的包的详细信息
    author = '不忘初心',   #发布的作者信息
    author_email = '2093804917@qq.com',
    py_modules = ['__init__', 'engine', 'main', 'models']  #发布的包的模块文件列表
)