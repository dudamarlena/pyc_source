from setuptools import setup, find_packages

from codecs import open
from os import path

readme_folder = path.abspath(path.dirname(__file__))

with open(path.join(readme_folder, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wlin',
    version='0.0.0',
    description='Soon',
    long_description=long_description,
    url='https://github.com/monzita/wlin',
    author='Monika Ilieva',
    author_email='hidden@hidden.com',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 3.6'
    ],
    license='GNU General Public License v3 or later (GPLv3+)',
    keywords='windows linux',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'venv']),
)