#-*- coding:utf-8 -*-
from setuptools import setup, find_packages
setup(  
    name = 'modbusStructConvert',  
    version = '1.0',
    keywords = ('modbusStructConvert'),  
    description = u'modbus寄存器值与可读值之间进行转换,支持各种寄存器地址顺序',  
    license = 'MIT License',  
    install_requires = ['chardet'],  
    packages = ['src'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'Ray Wong',  
    author_email = 'feelingswl@gmail.com',
    #url = 'https://github.com/mouday/chinesename',
    # packages = find_packages(include=("*"),),  
)