from distutils.core import setup

setup(
      name = 'wyvern',
      packages = ['wyvern'],
      version = '0.1.0',
      author = 'Daniel Moran',
      author_email = 'danxmoran@gmail.com',
      url = 'https://github.com/danxmoran/wyvern',
      requires = [
      	'requests (>=1.1.0, <2.0.0)',
      	'requests_oauthlib (==0.3.0)'
      	],
      keywords = ['Twitter', 'API', 'Twitter API', 'REST API'],
      description = 'Python 3k wrapper for the Twitter API',
      long_description = open('README.txt').read(),
      classifiers = [
      	'Programming Language :: Python',
      	'Programming Language :: Python :: 3',
      	'Development Status :: 3 - Alpha',
      	'Operating System :: OS Independent',
      	'License :: OSI Approved :: MIT License',
      	'Topic :: Internet',
      	'Topic :: Communications :: Chat',
      	'Intended Audience :: Developers',
      	'Intended Audience :: Science/Research'
      	]
      )
