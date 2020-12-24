# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/15 10:46
# !/usr/bin/python

from distutils.core import setup

setup(
    name="guoya-api",  # 这里是pip项目发布的名称
    version="0.0.4",  # 版本号，数值大的会优先被pip
    keywords=["init", "auto-api-test"],
    description="to simplify auto test",
    long_description="A init package,to simplify develope auto test",
    license="MIT Licence",

    url="https://github.com/LudvikWoo/guoya-tools",  # 项目相关文件地址，一般是github
    author="wuling",
    author_email="wuling@guoyasoft.com",
    # data_files =['init_tool.py'],
    # packages=['tools'],
    platforms="python",
    install_requires=[
        'guoya-tools',    # 中文转拼音
        'Flask==1.1.1'
    ]
)