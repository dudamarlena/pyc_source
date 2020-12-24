import os
from distutils.core import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
long_description = 'parse yaml front matter and write osx tags'

if os.path.exists('README.rst'):
    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='tagify',
    version='0.2.7',
    description='parse yaml front matter and write osx tags',
    long_description=long_description,
    author='Simon Breiter, Emanuele Mazzotta',
    author_email='hello@simonbreiter.com, hello@emanuelemazzotta.com',
    license='MIT',
    url='https://gitlab.com/simonbreiter/tagify',
    keywords=['yaml', 'front matter', 'osx', 'tags'],
    classifiers=[],
    py_modules=['tagify'],
    entry_points={
        'console_scripts': [
            'tagify=tagify:main',
        ],
    },
)
