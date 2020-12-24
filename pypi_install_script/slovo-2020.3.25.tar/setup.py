"""
slovo
~~~~~
slovo's propose is mainly for making words.
"""

from setuptools import setup, find_packages
from os import path

directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="slovo",
    version=__import__("slovo").__version__,
    description="Making words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Oleg Butuzov",
    author_email="butuzov@made.ua",
    url="https://github.com/butuzov/slovo",
    platforms=["OS Independent"],
    keywords=["words", "dictionalies"],
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests']),
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Education",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
