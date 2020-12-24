from setuptools import setup, find_packages

setup(
    name='parser-main',
    version='3.2.R',
    packages=find_packages(),
    url='',
    license='',
    author='Ivan Bondarenko',
    author_email='ivan.frinom@gmail.com',
    description='',
    install_requires=[
        'pymysql',
        'requests',
        'bs4',
        'openpyxl',
    ]
)
