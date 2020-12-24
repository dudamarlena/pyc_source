# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='s3_log',

    version='0.0.4',

    description='s3 log utils',
    long_description='s3 log utils',

    url='https://github.com/xiachufang/s3-log',

    # Author details
    author='Kebin',
    author_email='kebin@xiachufang.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['pytz', 'boto3'],
    keywords='s3 log',
    include_package_data=True
)
