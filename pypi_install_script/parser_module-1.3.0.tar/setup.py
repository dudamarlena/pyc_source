from setuptools import setup, find_packages

setup(
    name='parser_module',
    version='1.3.0',
    packages=find_packages(),
    author_email='ivan.frinom@gmail.com',
    install_requires=[
        'ParSer-Libraries>=1',
        'requests',
        'bs4',
    ]
)