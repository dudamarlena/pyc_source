from distutils.core import setup
setup(
    name='bcwyx',  # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是一个测试小模块',  #描述
    author='ffwwwyx', # 作者
    author_email='2668705579@qq.com',
    py_modules=['bcwyx.demo1','bcwyx.demo2'] # 要发布的模块
)
