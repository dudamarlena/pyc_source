#!/usr/bin/env python3
# coding:utf-8
"""
@file: setup.py
@time: 2018/8/31 16:12
@desc:
"""

from setuptools import setup, find_packages

setup(
    name='add-demo',
    version='1.0.0',
    description='just for test',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        ],
    install_requires=[],  # install_requires字段可以列出依赖的包信息，用户使用pip或easy_install安装时会自动下载依赖的包
    author='whl',
    url='https://github.com',
    author_email='1065116100@qq.com',
    license='MIT',
    packages=find_packages(),  # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    include_package_data=False,
    zip_safe=True,
    )