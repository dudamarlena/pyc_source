from setuptools import setup

setup(name = "Jump Bike DC API Wrapper",
    url = 'https://github.com/Leschonander/Jump-Bike-D.C-Python-API-Wrapper',
    author = "Lars E. Schonander",
    author_email = 'leschonander@gmail.com',
    packages=['src'],
    install_requires=['requests'],
    version = '0.1',
    license = 'MIT',
    description = "Python Wrapper for Jump Bike D.C's open API." 
)