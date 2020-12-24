# Copyright (c) 2018 BeDigital, UAB.
# All Rights Reserved.

from setuptools import find_packages, setup


setup(
    name='digital',
    version='0.0.1.3',
    description='Utility to interact with services and automate workflows.',
    long_description='',
    url='https://gitlab.com/xybid/digital',
    author='Mindey',
    author_email='mindey@qq.com',
    license='ASK FOR PERMISSIONS',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        "pandas",
        "rocketchat_API",
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
