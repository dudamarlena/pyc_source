import setuptools
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(name="marcusdb",
    version="1.0.2",
    description="A python library for https://db.marcusweinberger.repl.co/",
    long_description=read("README.md"),
    url="https://github.com/AgeOfMarcus/mdb",
    author="AgeOfMarcus",
    author_email="marcus@marcusweinberger.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=['requests', 'jsonpickle']
)