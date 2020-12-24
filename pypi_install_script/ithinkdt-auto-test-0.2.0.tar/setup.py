# !usr/bin/env python
# _*_ coding: utf-8 _*_

from setuptools import setup
from setuptools import find_packages


setup(
    name='ithinkdt-auto-test',  # 项目代码所在目录，也是pip 要上传的项目名称
    version='0.2.0',  # 工具的版本号
    description='auto test libs',
    long_description='python libs of auto test include ddt, base, run_set, upload',
    license='MIT',
    author='huiLi',
    author_email='lihui@ithinkdt.com',
    packages=find_packages(where='./ithinkdt-auto-test'),  # 查找包的路径
    package_dir={'': 'ithinkdt-auto-test'},      # 包的root 路径映射到的实际路径
    install_requires=['selenium', 'pywin32'],
    platforms='any'
)
