from setuptools import setup


try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""


setup(name='DowPy',
      version='0.1.6',
      description='Module for downloading files over HTTP(s) efficiently',
      url='https://pypi.org/project/dowpy/',
      author='JohnBrunelle',
      author_email='devjohnb@gmail.com',
      license='MIT',
      packages=['dowpy'],
      long_description=long_description,
      long_description_content_type='text/x-rst',
      install_requires=['requests'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
