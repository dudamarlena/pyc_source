from setuptools import setup

setup(
    name='Film analysis',
    author='Sydorenko Valeriia',
    author_email='jladan@uwaterloo.ca',
    packages=['film'],
    install_requires=['pandas', 'matplotlib','numpy'],
    version='1',
    license='MIT',
    description='This package analyzes data of films and directors',
)