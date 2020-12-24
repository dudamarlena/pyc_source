#引入构建包信息的模块
from distutils.core import setup

#定义发布的包文件信息
setup(
    name="yingzi",#发布的包文件名称
    version="1.0",#发布的包的版本序列号
    description="我的测试包",#发布包的描述信息
    author="影子",#发布包的作者信息
    author_email="yingzi@163.com",#作者联系邮箱
    py_modules=['__init__','game_sprites','game_engine','main','setup']#发布的包中的模块文件列表
)