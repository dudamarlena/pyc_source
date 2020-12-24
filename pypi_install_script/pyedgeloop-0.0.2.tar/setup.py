import setuptools
from distutils.core import setup
import pyedgeloop

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyedgeloop',
    author = 'Aditya Dutt',
    author_email = 'adityadutt1996@gmail.com',
    description="An efficient and fast library to detect loops, edges and outer boundary in binary images",
    long_description=long_description,    
    long_description_content_type="text/markdown",    
    version='0.0.2',
    packages=setuptools.find_packages(),
    install_requires=['numpy','opencv-python','scipy'],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
      "package": pyedgeloop
	}
)