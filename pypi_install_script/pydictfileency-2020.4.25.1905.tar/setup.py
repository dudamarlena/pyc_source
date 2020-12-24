
import setuptools
#from setuptools import setup

setuptools.setup(
    name='pydictfileency',
    scripts=[] ,
    version='2020.04.25.1905',
    author='Hengyue Li',
    author_email='hengyue.li@hengyue.li',
    packages=setuptools.find_packages(),
    license='LICENSE.md',
    description='A simple API used to encrypt the python dict into a file using AES256.',
    long_description=open('README.md',encoding="utf8").read(),
    long_description_content_type="text/markdown",
    install_requires=['pycryptodome==3.9.7'],
    python_requires='>=3.5',
    url = "https://github.com/HengyueLi/easycon",
)
