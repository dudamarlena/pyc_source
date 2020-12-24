try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(name="pvviewer",
      version="0.1",
      description="View Protein Stuctures in Jupyter Notebooks",
      author="Marco Biasini",
      url="https://github.com/biasmv/pv",
      py_modules=["pvviewer"])
