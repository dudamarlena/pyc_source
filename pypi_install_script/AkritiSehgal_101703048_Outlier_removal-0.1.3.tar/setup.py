
"""
Created on Sun Feb  9 

@author: akriti
"""
#Made by Akriti Sehgal 101703048
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AkritiSehgal_101703048_Outlier_removal",
    version="0.1.3",
    author="Akriti Sehgal",
    author_email="akritisehgal9@gmail.com",
    description="A small example package for removal of outliers in the given dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/AkritiSehgal/outlier_removal_101703048/archive/v_01.3.tar.gz",
    keywords = ['command-line', 'Outliers', 'outlier-removal','row-removal'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
