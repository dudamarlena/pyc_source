# !usr/bin/env python
# _*_ coding: utf-8 _*_

from distutils.core import setup
from setuptools import find_packages

setup(
    name='ithinkdtTestLib',  # 项目代码所在目录，也是pip 要上传的项目名称
    version='0.1.0',  # 工具的版本号
    # keywords=('pip', 'os'),
    description='A python lib for test',
    long_description='This is a python lib for test',
    license='MIT',

    url='https://gitee.com/xjyuan/mylib',  # homepage
    author='xjyuan',
    author_email='yuanxujuan@ithinkdt.com',

    packages=find_packages(where='./src'),  # 查找包的路径
    include_package_data=False,
    platforms='any',
    install_requires=[],  # 数组包含的是pip 项目引用到的第三方库，包名及版本号
    # scripts=[],
    # entry_points={
    #     'console_scripts':['initcli=initcli.cli:main']
    # },

    package_dir={'': 'src'},  # 包的root 路径映射到的实际路径
    package_data={'data': []},


)
