import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="powerzip",
    version="0.0.1",
    author="acgmohu",
    author_email="acgmohu@gmail.com",
    description=("A parser for AndroidManifest.xml"),
    license="Apache",
    keywords="zip",
    url="https://github.com/acgmohu/powerzip",
    py_modules=["powerzip"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
