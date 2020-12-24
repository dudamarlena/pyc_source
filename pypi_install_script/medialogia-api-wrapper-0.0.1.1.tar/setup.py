from setuptools import setup, find_packages

setup(
    name='medialogia-api-wrapper',
    version='0.0.1.1',
    packages=find_packages(),
    install_requires=[
        'zeep>=3.4.0'
    ],
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/medialogia-api-wrapper',
)
