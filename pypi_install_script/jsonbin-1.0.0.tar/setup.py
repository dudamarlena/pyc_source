import setuptools
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(name="jsonbin",
    version="1.0.0",
    description="A python library for https://jsonbin.marcusweinberger.repl.co/",
    long_description=read("README.md"),
    url="https://github.com/AgeOfMarcus/jsonbin",
    author="AgeOfMarcus",
    author_email="marcus@marcusweinberger.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=['requests', 'jsonpickle']
)