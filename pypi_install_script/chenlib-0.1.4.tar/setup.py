# /usr/bin/env == python3.7
# -*- coding=utf-8 -*-
# @author      : quinn7solomon
# @email       : quinn.7@foxmail.com
# @starting    : 2020-04-11
# @environment : PyCharm && VsCode

# setup.py
import pathlib
from setuptools import setup, find_packages

readme_path = str(pathlib.Path.cwd().joinpath('README.md'))

setup(
    name='chenlib',
    version='0.1.4',
    keywords=('pip', 'chenlib'),
    description='Optimizes and encapsulates tools to make them more powerful',
    # long_description='Optimizes and encapsulates tools to make them more powerful',
    long_description=open(readme_path, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='None',

    url='https://github.com/quinn7solomon/chenlib',
    author='quinn7solomon',
    author_email='quinn.7@foxmail.com',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[]
)

