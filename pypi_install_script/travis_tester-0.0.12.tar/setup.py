from setuptools import setup
import re

# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package#7071358
VERSIONFILE = "mypackage/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." %
                       (VERSIONFILE,))

setup(name='travis_tester',
      version=verstr,
      description='Testing git and deployment stuff',
      long_description="Nothing",
      url='https://github.com/MatthewGilbert/testing',
      author='Matthew Gilbert',
      author_email='matthew.gilbert12@gmail.com',
      license='MIT',
      platforms='any',
      packages=['mypackage', 'mypackage.tests'],
      zip_safe=False)
