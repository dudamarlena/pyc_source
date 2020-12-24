from setuptools import setup, find_packages
from Cython.Build import cythonize

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="regstring",
    version="1.0.2",
    author="l0n0l",
    author_email="1038352856@qq.com",
    description="A simple lib for generate regex string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l00n00l/regex_string.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    ext_modules=cythonize("regstring.cpp"))
