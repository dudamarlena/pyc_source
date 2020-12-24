from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="UnitSkuMasterPyforest",
    version="0.0.3",
    author="Dylan",
    author_email="lidelin@netsdl.com",
    description="test pypi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lidelin@git.netsdl.com/lidelin/pyforest_unitskumaster",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords='pyforest unitskumaster'
)