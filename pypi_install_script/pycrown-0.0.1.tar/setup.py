import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycrown",
    version="0.0.1",
    author="adrianhdez929",
    author_email="adrianhdez929@gmail.com",
    description="A python package, fork of the python bitcoin package, and adapted to Crown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianhdez929/pycrown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
