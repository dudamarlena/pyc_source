"""Setup file for aqara package."""
from setuptools import setup, find_packages

setup(name='pyaqara',
 version='0.24.1',
 description='Python API for interfacing with the Aqara gateway',
 url='https://github.com/javefang/pyaqara',
 download_url="https://github.com/javefang/pyaqara/tarball/0.24.1",
 author='Xinghong Fang',
 author_email= 'xinghong.fang@gmail.com',
 license='MIT',
 packages=['aqara'],
 keywords = ['aqara', 'home', 'automation', 'sensor'],
 install_requires=['pycrypto', 'PyDispatcher']
)
