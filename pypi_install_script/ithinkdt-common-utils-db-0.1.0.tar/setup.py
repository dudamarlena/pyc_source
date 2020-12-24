# !usr/bin/env python
# _*_ coding: utf-8 _*_

from setuptools import setup
from setuptools import find_packages


setup(
    name='ithinkdt-common-utils-db',  # 项目代码所在目录，也是pip 要上传的项目名称
    version='0.1.0',  # 工具的版本号
    description='python utils of db connect',
    long_description='python libs of connect database',
    license='MIT',
    author='huiLi',
    author_email='lihui@ithinkdt.com',
    packages=find_packages(where='./ithinkdt-common-utils-db'),  # 查找包的路径
    package_dir={'': 'ithinkdt-common-utils-db'},      # 包的root 路径映射到的实际路径
    install_requires=['pymysql'],
    platforms='any'
)
