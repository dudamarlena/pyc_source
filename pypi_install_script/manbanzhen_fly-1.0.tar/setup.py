# 引入构建包信息的模块
from distutils.core import setup

# 定义发布的包文件的信息

setup(
    name="manbanzhen_fly",      # 发布的包文件名
    version = "1.0",              # 发布的包的版本序号
    description="一个2d的飞车游戏，玩了之后松不开手", #发布包的描述信息
    author="慢半帧",        # 发布包的作者信息
    author_email="1441576268@qq.com",   # 作者联系邮箱信息
    py_modules=["game_engine","game_sprites"]    #发布的包中的模块文件列表


)
