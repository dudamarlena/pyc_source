# -*- coding: utf-8 -*-
from distutils.core import setup

readme = """
## Block Chain Tools

Block chain parser implementation written in python. Contains examples for Bitcoin and Litecoin.

    blocktools package - classes for reading blocks and transaction data from blockchain files
    bin/sight.py - example implementation, console script to parse blockchain files

## Usage

`python bin/sight.py blk00001.dat`

or if installed:

`sight blk00001.dat`

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

Alex Gorale, original author - https://github.com/tenthirtyone/blocktools

Hendrik 'Bloody' Schumann, cleanup, pypi packaging, various improvements

## License

BSD 3

"""

setup(
    name='blocktools',
    version='0.1.3',
    author="Hendrik 'Bloody' Schumann, Alex Gorale",
    author_email='pypi@schumann.pw',
    packages=['blocktools'],
    scripts=['bin/sight.py'],
    url='https://github.com/Nyancoins/blocktools',
    license='BSD3',
    description='Bitcoin blockchain parser',
    long_description=readme,
)