from setuptools import setup

import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="treeart",
    packages=["treeart"],
    version="0.0.2",
    license="MIT",
    description="Draw ASCII trees easily",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/taliesinb/treeart",
    download_url="https://github.com/taliesinb/treeart/archive/v0.0.1.tar.gz",
    author="Taliesin Beynon",
    author_email="contact@taliesin.ai",
    keywords=["ascii", "tree", "art", "binary"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)