#引入构建包信息的模块
from distutils.core import setup

#定义发布的包文件的信息
setup(
    name = "yh_catch_apple",#发布的包文件的名称
    version = "1.0",#发布包的版本序号
    discription = "我的接苹果游戏包",#发布包的描述信息
    author = "月亮守护神",#发布包的作者信息
    author_email = "609940648@qq.com",#作者联系邮箱信息
    py_modules = ["__init__","game_engine","main","models","setup"]
)