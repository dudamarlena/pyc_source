from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tom-gemini',
    version='0.1.0',
    description='Gemini Observatory module for the TOM Toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://tomtoolkit.github.io',
    author='Bryan Miller',
    author_email='ariba@lco.global',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    keywords=['tomtoolkit', 'astronomy', 'astrophysics', 'cosmology', 'science', 'fits', 'observatory', 'gemini'],
    packages=find_packages(),
    install_requires=[
        'tomtoolkit',
        'gsselect',
    ],
    include_package_data=True,
)
