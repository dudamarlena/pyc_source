from setuptools import setup, find_packages
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    # 以下为必需参数
    name='ethwallet--sdk',  # 模块名
    version='0.0.2',  # 当前版本
    description='SDK for ETH Wallet(以太坊钱包)',  # 简短描述
    packages=['ethwlt_sdk'], # 单文件模块写法
    install_requires=['web3'],
    # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法

    # 以下均为可选参数
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com', # 主页链接
    author='garder', # 作者名
    author_email='gaodelong01@163.com', # 作者邮箱
    classifiers=[
        'Intended Audience :: Developers', # 模块适用人群
        'License :: OSI Approved :: MIT License' # 模块的license
        ],
    keywords='blockchain eth wallet',  # 模块的关键词，使用空格分割
    )