# 引入构建包信息模块
from distutils.core import setup

# 定义发布的包文件的信息
setup(
    name="fight_plane",
    version="1.0",
    description="娇娇的飞机大战",
    author="淡陌",
    author_email="2293693518@qq.com",
    py_modules=['__init__', 'game_engine', 'game_sprites', 'main']
)
