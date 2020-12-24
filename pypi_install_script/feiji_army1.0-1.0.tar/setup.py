#引入构建包信息的模块
from distutils.core import setup
#定义发布的包文件的信息
setup(
    name = "feiji_army1.0", #发布的包文件名称
    version = "1.0", #发布的包的版本序号
    description = "我的测试包" , #发布包的描述信息
    author = "Ning_Caichen" ,#发布包的作者信息
    author_email = "975973347@qq.com" , #作者的联系邮箱信息
    py_modules = ['__init__','main','models','game_engine'] #发布的保重的模块文件列表
)