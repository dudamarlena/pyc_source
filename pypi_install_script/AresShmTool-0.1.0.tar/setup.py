# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='AresShmTool',
    version='0.1.0',
    description='Wizardquant tools utilities',
    long_description='Wizardquant tools utilities',
    author='fanyong',
    author_email='fanyong@wizardquant.com',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    url='http://183.234.21.121:10080/dataSource/WQDataTools/tree/feature/fanyong_dev/aresShmTools',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'pandas==0.23.4',
        'ctypes==1.1.0',
        're==2.2.1',
        'numpy==1.14.5',
        'weave==0.16.0'
    ]
)
