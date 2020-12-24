from distutils.core import setup

setup(
name='jasonmath', # 对外我们模块的名字
version='2.0', # 版本号
description='这是第一个对外发布的模块，测试哦', #描述
author='jason', # 作者
author_email='jason@gmail.com',
py_modules=['jasonmath.demo1'] # 要发布的模块
)