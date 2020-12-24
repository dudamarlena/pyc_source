# setup.py文件作用
# 	项目信息的配置文件
# 	这个里面最重要的是执行一个setup函数，通过这个函数来指明信息
# 使用方式
# from setuptools import setup
# setup(形参1=实参1，形参2=实参2)
# 	建议使用
from setuptools import setup


def readme_file():
    with open("D:\python\yutest\README.rst", "r", encoding="utf-8") as rf:
        return rf.read()
    pass


setup(name="yutest", version="1.0.1", description="这是一个牛逼的库"
      , packages=["yutest"], py_modules=["Tool"], author="yu",
      author_email="yua5726@gmail.com", long_description=readme_file(),
      url="https://github.com/AoXinYu/yutest/",LICENSE="MIT")
