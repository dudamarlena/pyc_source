import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'smktest',
  packages = ['smktest'], # this must be the same as the name above
  version = '0.1.5',
  description = 'This package offers a series of tests to create the correct Smoke Test of an application before uploading changes to production.',
  author = 'Cecilio Cannavacciuolo Diaz',
  author_email = 'cecilio.cannav@gmail.com',
  url = 'https://github.com/cecilio-cannav/smktest.git', # use the URL to the github repo
  license='MIT',
  keywords = ['smoketest', 'testing', 'python', 'smart',],
  python_requires='>=3',
)

install_requires = [
    'subprocess',
    'requests',
    'pytest',
    'pyhttptest',
]

