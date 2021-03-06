import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
]

setup(
    name="dictop",
    version="0.1.4",
    description="DICT-OPERATION allow you select data value from a dict-instance with dot separated path, and update.",
    long_description=long_description,
    url="https://github.com/appstore-zencore/dictop",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['dictop'],
    requires=requires,
    install_requires=requires,
    packages=find_packages(".", exclude=["tests"]),
    py_modules=["dictop"],
)