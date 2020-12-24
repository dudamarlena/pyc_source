from setuptools import setup, find_packages
from os import path

import mirmag


setup(
    name='miRMag',
    version=mirmag.__version__,
    packages=find_packages(),
    url='https://github.com/Repoxitory/miRMag',
    license='MIT',
    author='vps',
    author_email='pavel.vorozheykin@gmail.com',
    description='Some tools to process miRNA sequences, to predict them and to explore their features.',
    long_description=open(path.join(path.dirname(__file__), 'README.rst')).read(),
    install_requires=[],
    include_package_data=True
)
