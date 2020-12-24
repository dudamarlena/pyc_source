from setuptools import setup

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Python Software Foundation License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development",
]

setup(
    name="pegen",
    version="0.0",
    description="PEG parser generator",
    author="Guido van Rossum, Pablo Galindo Salgado, Lysandros Nikolau",
    author_email="guido@python.org",
    url="https://github.com/gvanrossum/pegen",
    license="PSF",
    packages=["pegen"],
    classifiers=classifiers,
)
