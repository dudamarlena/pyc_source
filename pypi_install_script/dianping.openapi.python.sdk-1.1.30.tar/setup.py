from setuptools import setup, find_packages

setup(
name='dianping.openapi.python.sdk',
version='1.1.30',
keywords=('dianping', 'openapi'),
description='dianping openapi python sdk',
license='MIT License',
packages=find_packages(),
install_requires=['requests']
)