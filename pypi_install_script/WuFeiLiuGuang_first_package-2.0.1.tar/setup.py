# Version : 2.0.0
# Author : LiuWei
# Date : 2019.11.07

#!/user/bin/python
#-*- coding:uft-8 -*-

from distutils.core import setup

with open('README') as file:
	readme = file.read()

setup(
    name='WuFeiLiuGuang_first_package',
    version='2.0.1',
    packages=['wargame'],
    url='https://testpypi.python.org/pypi/WuFeiLiuGuang_first_package/',
    license='LICENSE.txt',
    description='test pkg ignore',
    long_description=readme,
    author='WuFeiLiuGuang',
    author_email='20611873@qq.com'
)
