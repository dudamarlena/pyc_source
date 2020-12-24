# Copyright (c) 2019 Mindey.
# All Rights Reserved.

from setuptools import find_packages, setup

setup(
    name='dynapi',
    version='0.0.2',
    description='Extras for dyanlist API wrapper.',
    url='https://gitlab.com/mindey/dynapi',
    author='Mindey',
    author_email='mindey@qq.com',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        "requests",
        "dynalist",
    ],
    extras_require={
        'develop': [
            'pre-commit==1.18.3',
            'coverage==4.5.4',
            'flake8==3.7.8',
            'isort==4.3.21',
        ],
    },
    zip_safe=False
)
