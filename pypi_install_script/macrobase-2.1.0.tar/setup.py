from setuptools import setup, find_packages

setup(
    name='macrobase',
    version='2.1.0',
    packages=find_packages(),
    url='https://github.com/mbcores/macrobase',
    license='MIT',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='Macrobase framework for build mAcroservices',
    install_requires=[
        'macrobase-driver>=2.0.0,<3.0.0',
        'structlog==19.2.0'
    ]
)
