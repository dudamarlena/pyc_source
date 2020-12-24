from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="qlite",
    version="0.0.6",
    author="BorisPlus",
    author_email="boris-plus@mail.ru",
    description="QLite is a lite project of SQLite ORM at Python3, as lite ORM for lite SQL.",
    long_description=long_description,
    url="https://github.com/BorisPlus/otus_webpython_005",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Database",
    ],
)
