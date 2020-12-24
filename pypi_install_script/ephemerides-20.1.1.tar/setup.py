from setuptools import setup

version = '20.1.1'

setup(
   name = 'ephemerides',
   version = version,
   author = 'R. Thomas, T. Berg',
   author_email = 'the.spartan.proj@gmail.com',
   packages = ['ephemerides'],
   description = 'ESO ephemerides in Python',
   url = 'https://astrom-tom.github.io/ephemerides/build/html/index.html',
   python_requires = '>=3.6',
   install_requires = [
        "requests >= 2.22.0",
        "bs4 >= 0.0.1",
       ],
   include_package_data=True,
)
