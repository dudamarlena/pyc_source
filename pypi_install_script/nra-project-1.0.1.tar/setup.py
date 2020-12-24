import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="nra-project",
    version="1.0.1",
    description="library and helper for analitycs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nim4n136/nra_project",
    author="nim4n136",
    author_email="nim4n136@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    packages=["nra_project"],
    include_package_data=True
)