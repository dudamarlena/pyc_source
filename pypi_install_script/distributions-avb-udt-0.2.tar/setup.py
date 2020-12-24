from setuptools import setup

with open("README.rst", "r") as fi:
    long_description = fi.read()
    
    
setup(name='distributions-avb-udt',
      version='0.2',
      description='Distributions',
      packages=['distributions'],
      long_description=long_description,
      python_requires=">=3.6",
      license="GNU GENERAL PUBLIC LICENSE v3.0",
      zip_safe=False)
