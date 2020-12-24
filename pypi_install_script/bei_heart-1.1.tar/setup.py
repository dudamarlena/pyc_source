'''
构造/构建：build
打包：package
'''

# 引入需要的构建函数
from distutils.core import setup

setup(
    name='bei_heart',
    version='1.1',
    description='表白',
    author='xzh',
    author_email='15516989972@163.com',
    py_modules=['__init__','data','views']
)    