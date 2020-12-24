'''
重点：构建和打包 build/package
'''

#引入需要的构建函数
from distutils.core import setup

setup(
    name = "wdj",
    version="1.0",
    discription="测试程序",
    author="愚",
    author_email="1851524312@qq.com",
    py_modules=["__init__","main","data","menus","energy","service"]


)