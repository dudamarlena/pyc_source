#from distutils.core import setup
from setuptools import setup

setup(
    name='myfirstdemo2', #应用名
    author='hc',
    author_email='crystal910901@foxmail.com',
    version='1.0.0',
    description='test_demo',
    url='http://www.haocang.com',
    license='MIT',
    packages=['demo1','demo2'], #包括在安装包内的python包
    py_modules=['demo1.helloworld'],
    #install_requires=[], #安装包所依赖的其他包
    #entry_point={'console_scrpits':['demo1=demo1.command_line:main']} #执行指定包下的py文件里的main函数




)