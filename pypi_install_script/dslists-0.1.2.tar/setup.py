from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dslists',
    packages=['dslists'],
    version='0.1.2',
    include_package_data=True,
    license='MIT',
    description='A collection of useful lists for data science.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matt Mackenzie',
    author_email='mbm2228@columbia.edu',
    url='https://github.com/mbmackenzie/dslists',
    download_url='https://github.com/mbmackenzie/dslists/archive/v0.1.2.tar.gz',
    keywords=['data', 'analytics'],
    install_requires=[
        'pandas'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
