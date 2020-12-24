from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bottleapp",
    version="0.0.1",
    description="Object-oriented extension to bottle, allowing your app to be a class instance and providing automatic path generation.",
    long_description=long_description,
    url="https://github.com/lainproliant/bottleapp",
    author="Lain Supe (lainproliant)",
    author_email="lainproliant@gmail.com",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: Bottle",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="bottle oop web",
    py_modules=["bottleapp"],
    install_requires=["bottle", "xeno"],
    entry_points={},
)
