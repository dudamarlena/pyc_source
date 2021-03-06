import os.path

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='gzlog',
      version="0.2",
      author="Mike Spindel",
      author_email="mike@spindel.is",
      license="MIT",
      keywords="zlib logging",
      url="http://github.com/deactivated/python-gzlog",
      description='',
      packages=find_packages(exclude=['ez_setup']),
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Programming Language :: Python"])
