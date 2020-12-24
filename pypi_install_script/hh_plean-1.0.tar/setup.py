'''
构建：build
打包：package
'''
# 引入需要的构建函数
from distutils.core import setup

setup(
    name='hh_plean',
    version='1.0',
    description='飞机大战',
    author='纪念',
    author_email='111@qq.com',
    py_modules=['__init__', 'gamestart', 'game_sprites', 'game_engine']
)
