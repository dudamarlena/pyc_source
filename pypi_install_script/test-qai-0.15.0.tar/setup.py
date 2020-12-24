import os
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(here, "VERSION"), encoding="utf-8") as f:
    __version__ = f.read().strip()
    with open(
        os.path.join(here, "test_qai", "version.py"), "w+", encoding="utf-8"
    ) as v:
        v.write("# CHANGES HERE HAVE NO EFFECT: ../VERSION is the source of truth\n")
        v.write(f'__version__ = "{__version__}"')

setup(
    name="test-qai",
    packages=find_packages(),
    install_requires=[
                        "essential-generators==0.9.2",
                        "requests==2.22.0",
                        "tqdm==4.36.1",
                        "pyfunctional==1.2.0",
                    ],
    author="Qordoba",
    author_email="melisa@qordoba.com",
    url="https://github.com/melisa-qordoba/test.qai",
    version=__version__,
    license="unlicensed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.4",
)
