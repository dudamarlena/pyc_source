import setuptools.command.test
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(name='tttb',
    version='0.0.2a1',
    description='Tensor Train Toolbox in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='http://github.com/tmolteno/tttb',
    author='Tim Molteno',
    author_email='tim@elec.ac.nz',
    license='GPLv3',
    install_requires=['numpy', 'scipy'],
    packages=['tttb'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research'])
