#!/usr/bin/python3
# coding: utf-8
from setuptools import setup,find_packages

setup(
    name='emailcli',
    version='0.1',
    author='GUCCI',
    author_email='guqi1986@126.com',
    url='https://github.com/gucci/emailcli',
    description='A email client in terminal',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    install_requires=['yagmail'],
    entry_points={
        'console_scripts': [
            'emailcli=emailcli:main',
        ]
    }
)
