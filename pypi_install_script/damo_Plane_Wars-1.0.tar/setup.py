# 引入构建包信息的模块
from distutils.core import setup

# 定义发布的包文件信息
setup(
    name="damo_Plane Wars",
    version="1.0",
    description="飞机大战",
    author="普通朋友",
    author_email="damo@qq.com",
    py_modules=['__init__', 'models', 'engine']
)