'''
重点：构建和打包
    构建/构造：build
    打包：package
'''

# 引入需要的构建函数
from distutils.core import setup

setup(
    name = 'plane_fxx',
    version = '1.0',
    description = '飞机大战',
    author = '六千l',
    author_email = '839011755@qq.com',
    py_modules = ['game_engine', 'game_main', 'game_sprites']
)