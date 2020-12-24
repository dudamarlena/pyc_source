import setuptools
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BLECommandlineTool", # Replace with your own username
    version="0.0.3",
    author="octavio",
    author_email="octavio.delser@gmail.com",
    description="commandlinetool and api for blemap backend services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/occy88/BLECommandlineTool",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
	"requests==2.22.0",
	"BLECryptracer-BLEMAP==0.0.7"
    ],
)
