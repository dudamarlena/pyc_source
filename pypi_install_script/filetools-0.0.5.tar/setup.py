# coding: utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filetools",
    version="0.0.5",
    author="Christian Winger",
    author_email="c@wingechr.de",
    description="file processing tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/filetools",
    project_urls={
        "Documentation": "https://filetools.readthedocs.io",
        "Source": "https://github.com/wingechr/filetools",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
