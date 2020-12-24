import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from  distutils.core import  setup
setup(
    name='xiaozhiling',#对外我们模块的名字
    version='1.0',#版本实在
    description='用于判断回文串的第一个对外模块，测试哦',
    author='肖智铃',#作者
    author_email='2842409558@qq.com',#邮箱
    py_modules=['qiuhuo.demo']#要发布的模块

    )