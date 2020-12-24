__author__ = 'zoulida'
from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "Santai",      #这里是pip项目发布的名称
    version = "3.0",  #版本号，数值大的会优先被pip
    keywords = ("pip", "santai","zoulida"),
    description = "",
    long_description = "",
    license = "MIT Licence",

    url = "https://github.com/zoulida/santai3",     #项目相关文件地址，一般是github
    author = "zoulida",
    author_email = "zoulida@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy"]          #这个项目需要的第三方库
)