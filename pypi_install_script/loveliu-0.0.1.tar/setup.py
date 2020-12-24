# -*- coding: utf-8 -*-
# from setuptools import setup
from distutils.core import setup
# 这两个的区别：https://segmentfault.com/q/1010000006681792

setup(
    name='loveliu',          # 模块名或者包名
    version='0.0.1',         # 版本号
    description='个人测试',  # 模块的描述
    # url='https://github.com/BigDataFounder/string2date',
    # download_url='https://github.com/ly0/baidupcsapi',
    author='liujiadon',    # 作者
    author_email='1548429568@qq.com',
    py_modules=["forever.love", "good"],  # 你的模块名
    license='MIT',
    packages=['forever'],
    # install_requires=['requests>=1.1.0'],
    keywords='test, love, API',
)