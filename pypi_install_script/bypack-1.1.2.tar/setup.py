from setuptools import setup

# read the contents of README.md
from os import path

directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bypack",
    version="1.1.2",
    description="The simple pack python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="htprogras",
    author_email="htprogras@gmail.com",
    license="MIT",
    packages=["bypack"],
    zip_safe=False,
)
