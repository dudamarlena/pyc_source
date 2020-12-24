'''
重点：构建和打包
    构建/构造：build
    打包：package
'''

#引入需要的构建函数
from distutils.core import setup

setup(
    name="manman_airplane",
    version="1.0",
    description="卡哇伊战斗飞机项目升级版",
    author="嘉宁",
    author_email="1228853142@qq.com",
    py_modules=["__init__","game_engine","game_main","game_sprites"]
)
