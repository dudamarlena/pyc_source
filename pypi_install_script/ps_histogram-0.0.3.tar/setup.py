from __future__ import print_function 
from setuptools import setup, find_packages 
import sys 
setup(name="ps_histogram", version="0.0.3", author="Ps",
		author_email="1596117875@qq.com", description="Histogram Equalization", license="MIT", url="https://github.com/ForeverPs",
	    long_description = 'Digital Image Processing, Histogram Equalization, Histogram Matching, Local Histogram Equalization,\
						   Image Segementation', packages=find_packages(), include_package_data=True,
		install_requires=[ 'numpy', 'matplotlib', 'cv2'], zip_safe=True,
	    classifiers=["Environment :: Web Environment", "Intended Audience :: Developers",
				   "Operating System :: Microsoft :: Windows :: Windows 10", "Topic :: Text Processing :: Indexing", "Topic :: Utilities",
				   "Topic :: Internet", "Topic :: Software Development :: Libraries :: Python Modules",
				   "Programming Language :: Python", "Programming Language :: Python :: 3",
				   "Programming Language :: Python :: 3.5", "Programming Language :: Python :: 3.6" ],)
