from distutils.core import setup
import setuptools

setup(
    name=		"nester-eslamturki",
    version=		"1.2.5",
    py_modules=		["nester"],
    author=		"eslamturki",
    author_email=	"eslam.turki@gmail.com",
    url=		"https://github.com/pypa/sampleproject",
    description=	"A simple printer of nested lists With tab Level",
    packages=setuptools.find_packages(),
    classifiers=[
                        "Programming Language :: Python :: 3",
                        "License :: OSI Approved :: MIT License",
                        "Operating System :: OS Independent",
    ],
    )
