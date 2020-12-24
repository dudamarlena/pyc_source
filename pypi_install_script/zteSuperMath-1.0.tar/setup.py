from distutils.core import setup
setup(
name='zteSuperMath', # 对外我们模块的名字
version='1.0', # 版本号
description='这是第一个对外发布的模块，测试哦', #描述
author='ChenJun', # 作者
author_email='chenjun8562@163.com',
py_modules=['zteSuperMath.demo1','zteSuperMath.demo2'] # 要发布的模块
)