import os
from setuptools import setup, find_packages
from discodash import version


def read_readme():
    return open("README.md").read()


setup(
    name="discodash",
    version=version,
    author="Epic",
    author_email="epic@tazhys.productions",
    description="Library to interact with the discodash site",
    license="BSD",
    keywords="discord.py discord discodash dashboard panel easy",
    url="https://discodashpanel.tk",
    packages=find_packages(),
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Topic :: Utilities",
    ], install_requires=['websockets', "discord.py"]
)
