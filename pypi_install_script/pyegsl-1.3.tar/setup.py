import setuptools
from distutils.core import setup, Extension
from pathlib import Path

def main():
    setup(name="pyegsl",
          version="1.3",
          description="Python easy interface to gsl",
          author="Heitor L. Werneck",
          author_email="heitorwerneck@hotmail.com",
          url='https://github.com/heitor57/pyegsl',
          license="MIT",
          packages=setuptools.find_packages(),
          long_description=Path("README.rst").read_text(encoding="utf-8"),
          long_description_content_type="text/x-rst",
          ext_modules=[Extension(
              "pyegsl.binomial", ["pyegsl/binomial.cpp"],
              libraries = ['gsl','gslcblas'])])

if __name__ == "__main__":
    main()

