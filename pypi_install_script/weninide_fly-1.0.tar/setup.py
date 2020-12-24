#引入构建包信息的模块
from distutils.core import  setup

#定义发布包的文件的信息
setup(
    name ="weninide_fly",
    version= "1.0",
    description="飞机大战",
    author = "维尼熊",
    author_email = "wenini@163.com",
    py_modules = ['__init__','engine','font','main','model']
)