from setuptools import setup, find_packages

import versioneer


setup(
    name="exconfig",
    description="Configuration",
    long_description=open("README.rst", encoding="utf-8").read(),
    author="Eric Hutton",
    author_email="huttone@colorado.edu",
    url="http://csdms.colorado.edu",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=open("requirements.txt", "r").read().splitlines(),
    setup_requires=[],
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
