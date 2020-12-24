import os
from setuptools import setup

# The directory containing this file
HERE = os.path.dirname(os.path.abspath(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md"), "r") as f:
    README = f.read()

# This call to setup() does all the work
setup(
    name="sz-calculator",
    version="0.0.3",
    description="Cool Calculator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/stonezhong/pythondemos/tree/master/sz_calculator",
    author="Stone Zhong",
    author_email="stonezhong@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["sz_calculator"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "sz-calculator=sz_calculator.__main__:main",
        ]
    },
)
