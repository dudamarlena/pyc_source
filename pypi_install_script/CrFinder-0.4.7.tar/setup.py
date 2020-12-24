from setuptools import setup

setup(
    name='CrFinder',
    version='0.4.7',
    packages=['crfinder'],
    url='https://gitlab.com/Unkraut/crfinder',
    description='Utility for finding color references in a collection RAW photgraphs and creating .icc profiles.',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    long_description=open('README.md').read(),
    install_requires=['opencv-python', 'numpy', 'rawkit', 'matplotlib', 'scipy', 'colormath', 'tifffile', 'imutils', 'python-igraph'],
    entry_points={
        'console_scripts': ['crfinder=crfinder.crfinder:main',]},
)

