from setuptools import setup

setup(name='PyGsheetAPI',
      version='0.1',
      description='Python Gsheet Wrapper Library',
      url='http://github.com/samlazrak/pygsheet-api',
      author='Sam Lazrak',
      author_email='samlazrak@outlook.com',
      license='MIT',
      packages=['PyGsheetAPI'],
      install_requires=[
        'google-api-python-client',
        'oauth2client'
      ],
      zip_safe=False)
