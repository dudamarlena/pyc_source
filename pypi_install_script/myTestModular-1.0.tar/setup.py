#coding=utf-8
from distutils.core import setup
setup(
name='myTestModular', # 对外我们模块的名字
version='1.0', # 版本号
description='这是第一个对外发布的模块，测试哦', #描述
author='L_zr', # 作者
author_email='769975307@qq.com',
py_modules=['myTestModular.demo1'] # 要发布的模块
)