# _*_coding:utf-8_*_
"""
@ProjectName: SmxUtils
@Author:  Javen Yan
@File: setup.py
@Software: PyCharm
@Time :    2020/4/27 上午11:22
"""
from setuptools import setup

setup(
    name="SmxUtils",
    version="1.0.0",
    description="SM Secret Utils",
    url="https://github.com/yanzongzhen/SmxUtils",
    author="yanzongzhen",
    author_email="yanzongzhen127@outlook.com",
    license="MIT",
    packages=["SmxUtils"],
    data_files=[("SmxUtils", ["SmxUtils/ICitySMX.so", "SmxUtils/sm2.h", "SmxUtils/sm3.h"])],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
