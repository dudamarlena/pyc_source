from setuptools import setup

setup(
  name = 'pyossboilerplate',
  packages = ['pyossboilerplate'],
  version = '0.2.1',
  description = 'Generates boilerplate for open source python projects.',
  long_description = open('README.rst', 'r').read(),
  author = 'Patrick Ayoup',
  author_email = 'patrick.ayoup@gmail.com',
  license = 'MIT',
  url = 'https://patrickayoup.github.com/pyoss-boilerplate',
  download_url = 'https://github.com/patrickayoup/pyoss-boilerplate/tarball/0.2.1',
  keywords = ['open source', 'boiler plate'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Topic :: Software Development :: Code Generators',
    'Topic :: Utilities'
  ],
  entry_points = {
      'console_scripts': [
          'pyossboilerplate = pyossboilerplate.main:run'
      ]
  },
)