# 引入构建包信息的模块
from distutils.core import setup

# 定义发布的包文件的信息
setup(
name = "PlanWars_test001",  # 发布的包文件名称
version = "1.0",   # 发布的包的版本序号
description = "我的个人测试包",  # 发布包的描述信息
author = "llf",   # 发布包的作者信息
author_email = "2367746876@qq.com",  # 作者联系邮箱信息
py_modules = ['__init__', 'start', 'game_engine', 
'game_sprites', 'data'],  # 发布的包中的模块文件列表
)
