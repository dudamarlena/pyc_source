#-*- coding:utf-8 -*-

#use 'python setup.py bdist_egg' to generate the egg file package
#use 'easy_install eggfile' to install the egg file to the python Lib

#or

#use 'python setup.py install' to install to the python Lib directly


from setuptools import setup, find_packages

setup(
    name='obssdk',
    version='3.0.3',
    packages=find_packages(),
    zip_safe=False,
    description='OBS Python SDK',
    author="HUAWEI",
    author_email="esdk@huawei.com",
    long_description='OBS Python SDK',
    license='GPL',
    keywords=('obs', 'python'),
    platforms='Independant',
    url='https://developer.huaweicloud.com/sdk?OBS',
)
