import os
import glob
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django_gmzoom_tools",
    version="1.2.0",
    description="Gmzoom project tools",
    license = "BSD",
    long_description=read('README'),
    keywords="django gmzoom tools",
    author="Alex Blagodarov",
    author_email="ablagodarov@gmail.com",
    url="http://otzhig.ru/dev",
    platforms=["any"],
    classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Web Environment",
                   "Framework :: Django",
                   "Intended Audience :: Developers",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Utilities"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
