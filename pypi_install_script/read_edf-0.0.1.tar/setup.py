from setuptools import setup
from pathlib import Path

VERSION = '0.0.1'


def read(filename: str):
    with open(Path(__file__).parent / filename, mode='r', encoding='utf-8') as f:
        return f.read()


setup(
    name='read_edf',
    packages=['read_edf'],
    version=VERSION,
    author='Vladimir Starostin',
    author_email='vladimir.starostin@uni-tuebingen.de',
    description='Simple .edf reader.',
    # long_description=read('README.md'),
    # long_description_content_type='text/markdown',
    license='MIT',
    # include_package_data=True,
    python_requires='>=3.6.*',
    install_requires=[
        'numpy>=1.16.0'
    ],
)
