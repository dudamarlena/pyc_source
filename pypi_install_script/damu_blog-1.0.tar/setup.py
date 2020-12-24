'''
重点：构建和打包
    构建/构造：build
    打包：package
'''

# 引入需要的构建函数
from distutils.core import setup

setup(
    name='damu_blog',
    version='1.0',
    description='个人博客项目',
    author='大牧',
    author_email='damu@163.com',
    py_modules=['__init__', 'models', 'views', 'tools', 'manager', 'data']
)
