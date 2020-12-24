from distutils.core import setup

setup(
    name='yujiaMath',  # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦',  #描述
    author='tom202457', # 作者
    author_email='yujia_hz@126.com',
    py_modules=['yujiaMath.demo1','yujiaMath.demo2'] # 要发布的模块
)
