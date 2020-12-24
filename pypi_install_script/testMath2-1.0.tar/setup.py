from distutils.core import setup

setup(
    name='testMath2', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='dj', # 作者
    author_email='wadelbj1@163.com',
    py_modules=['testmath.demo1','testmath.demo2'] # 要发布的模块
)
