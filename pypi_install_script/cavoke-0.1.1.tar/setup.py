import setuptools
import os
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

base_path = os.path.dirname(__file__)

# Get the version (borrowed from SQLAlchemy)
with open(os.path.join(base_path, "src", "cavoke", "__init__.py")) as fp:
    version = (
        re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S).match(fp.read()).group(1)
    )

setuptools.setup(
    name="cavoke",
    version=version,
    author="Alex Kovrigin",
    author_email="a.kovrigin0@gmail.com",
    description="Python library for easy creation of text-based and table games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cavoke-project/cavoke-lib/",
    packages=[
        "cavoke",
      ],
    package_dir={"": "src"},
    python_requires=">=3.7, <4",
    requires=["dataclasses"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
