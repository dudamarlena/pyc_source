from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fewsver",
    version="0.1.0",
    author="Georgios Boumis",
    author_email="boumis.georgios@gmail.com",
    description="Package for verifying GLOFFIS streamflow forecasts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
