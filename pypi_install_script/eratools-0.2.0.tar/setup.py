import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eratools",
    version="0.2.0",
    author="Chris Roth",
    author_email="chris.roth@usask.ca",
    description="A package extending xarray for use with ECMWF ERA model level data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://arggit.usask.ca/Chris/eratools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
