from os.path import isfile, join
from os import walk
import setuptools

from drftmpl import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()


def package_files(directories):
    paths = []
    for item in directories:
        if isfile(item):
            paths.append(join('..', item))
            continue
        for (path, directories, filenames) in walk(item):
            for filename in filenames:
                paths.append(join('..', path, filename))
    return paths


setuptools.setup(
    name="drftmpl",
    version=__version__,
    author="Mikele",
    author_email="blive200@gmail.com",
    description="Generate rest framework templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toyourheart163/drftmpl",
    install_requires=["jinja2"],
    packages=setuptools.find_packages(),
    package_data={
        "": package_files(["drftmpl/templates"])
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/drftmpl'],
    python_requires='>=3.6',
)
