import os

from setuptools import setup


def getversion():
    head = '__version__ = "'
    tail = '"\n'
    with open(os.path.join("append_db", "__init__.py")) as fp:
        for l in fp:
            if l.startswith(head) and l.endswith(tail):
                return l[len(head) : -len(tail)]
    raise Exception("__version__ not found")


setup(
    name="append_db",
    version=getversion(),
    description="AppendDb",
    url="https://github.com/kshramt/append_db",
    author="kshramt",
    packages=["append_db"],
    install_requires=[],
    classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    data_files=[(".", ["LICENSE.txt"])],
    zip_safe=True,
)
