

#引入构建包信息的模块
from distutils.core import setup

#定义发布的包文件信息
setup(
    name="wjc_01",
    verison="1.0",
    description="我的飞机大战",
    author="武军超",
    author_email="1505948599@qq.com",
    py_modules=['game_sprites', 'game_engine', 'main', "__init__", "set_up"]
    )
