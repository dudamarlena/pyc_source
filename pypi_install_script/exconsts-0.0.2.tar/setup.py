from distutils.core import setup

import exconsts


setup(
    name='exconsts',
    version=exconsts.__version__,
    packages=['exconsts'],
    url='https://github.com/lk-geimfari/exconsts',
    license='BSD-3 Clause',
    author=exconsts.__author__,
    author_email='likid.geimfari@gmail.com',
    description='A library that help you store your constants for applications in JSON file. '
)
