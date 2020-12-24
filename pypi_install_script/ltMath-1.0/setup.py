#coding=utf-8
from distutils.core import setup

setup(
    name="ltMath",   #对外我们模块的名字
    version="1.0",   #版本号
    description="这是第一个对外发布的模块，主要是测试",      #描述
    author="yinwenjing",   #作者
    author_email="2446220681@qq.com",   #作者邮箱
    py_modules=["ltMath.module_1","ltMath.module_2"]   #要发布的模块
)