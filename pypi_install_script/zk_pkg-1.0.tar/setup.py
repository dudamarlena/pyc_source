# 引入构建包信息的模块
from distutils.core import setup
# 定义发布的包文件的信息
setup(
name="zk_pkg",  # 发布的包文件名称
version="1.0",   # 发布的包的版本序号
description="飞机大战", # 发布包的描述信息
author="奈斯嗷",   # 发布包的作者信息
author_email="1176009143@qq.com", # 作者联系邮箱信息
py_modules=["__init__","data","game_engine","game_sprites","main","setup","image","wav"]# 发布的包中的模块文件列表
)