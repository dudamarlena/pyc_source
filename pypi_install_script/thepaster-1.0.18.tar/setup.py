import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'thepaster',
    version = '1.0.18',
    author = 'adder46',
    author_email = 'dedmauz69@gmail.com',
    description = ('client interface for https://dpaste.de/ pastebin'),
    license = 'MIT',
    keywords = 'client interface for https://dpaste.de/ pastebin',
    url = 'https://github.com/adder46/dpaster',
    packages=['dpaster', 'tests'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points = {
        'console_scripts': [
            'dpaster = dpaster.application:main'
        ],
    },
    install_requires=[
          'requests',
          'pyperclip',
          'click'
      ],
)
