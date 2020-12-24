from distutils.core import setup
setup(
  name = 'otus_search',
  packages = ['otus_search'],
  version = '0.0.3',
  license='MIT',
  description = 'Search links from web',
  author = 'vvscode',
  author_email = 'v.vanchuk@tut.by',
  entry_points={"console_scripts": ["otus-search=otus_search.search:main"]},
  url = 'https://github.com/vvscode/py--otus-search',
  download_url = 'https://github.com/vvscode/py--otus-search/blob/master/dist/otus-search-0.0.1.tar.gz?raw=true',
  keywords = ['otus', 'vvscode'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7'
  ],
)