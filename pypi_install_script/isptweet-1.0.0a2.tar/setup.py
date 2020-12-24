# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os

setup(
    name='isptweet',
    version='1.0.0-a2',
    description='Tweet @ your ISP whenever your internet speed is below what you pay for.',
    long_description=open('README.rst').read(),
    url='https://github.com/lschumm/isptweet/',
    author='Liam Schumm',
    author_email='liamschumm@icloud.com',
    license='GPL-3.0',
    install_requires=['speedtest-cli', 'python-twitter'],
    entry_points={
        'console_scripts': [
            'isptweet=main:main',
            ],
        },
)