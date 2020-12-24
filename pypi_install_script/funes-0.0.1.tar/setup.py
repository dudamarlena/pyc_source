from setuptools import setup

import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="funes",
    packages=["funes"],
    install_requires=["dill"],
    version="0.0.1",
    license="MIT",
    description="Decorator to memorize function computations permanently to disk.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/taliesinb/funes",
    download_url="https://github.com/taliesinb/funes/archive/v0.0.1.tar.gz",
    author="Taliesin Beynon",
    author_email="contact@taliesin.ai",
    keywords=["persistent", "cache", "hash", "stable", "archive", "memoize"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)