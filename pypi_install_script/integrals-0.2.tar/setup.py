
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='integrals',
     version='0.2',
     description='Numerical approximators to calculate the definit integral',
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=find_packages(),
     url="https://github.com/NullOsama/Integrals",
     author='Osama Maharmeh',
     author_email='maharmeh.osama98@gmail.com',
     classifiers=["Programming Language :: Python :: 3",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent"
    ],
     zip_safe=False,
     python_requires='>=3.6')