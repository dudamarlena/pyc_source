'''
重点：构建和打包
    构建/构造：build
    打包：package
'''

#引入需要构建的函数
from distutils.core import setup

setup(
    name="yuzihua_bolg",
    version="1.0",
    description="个人博客",
    author="折戟",
    author_email="969465519@qq.com",
    py_modules = ["__init__","data","engine","manager","views","main"]
)