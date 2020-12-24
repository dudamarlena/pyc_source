from setuptools import setup, find_packages

setup(name = 'pyparks',
    version = '0.1',
    description = 'Easy Python API for Themeparks',
    url = 'https://github.com/aschi2/pyparks',
    author='Austin',
    author_email='achi002@ucr.edu',
    license="MIT",
    packages = ['pyparks'],
    install_requires=[
        'pandas',
        'requests',
        'datetime',
        'unidecode'
    ],
    keywords='themepark disneyland wait time fastpass'



    )