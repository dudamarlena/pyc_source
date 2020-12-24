
from setuptools import setup

setup(
    name='da_gcp',
    version='2019.12.12',
    author='Matthew Trette',
    author_email='matt.trette@me.com',
    packages= ['da_gcp'],
    url='https://github.homedepot.com/Decision-Analytics/da_gcp/',
    license='LICENSE.txt',
    description='Python functions and wrappers for google.cloud python package',
    long_description='README.md',
    long_description_content_type='text/markdown',
    install_requires=[
        "google-cloud",
        "google-cloud-bigquery>=0.28.0",
        "google-cloud-storage>=1.6.0",
        "numpy>=1.13.0",
        "pandas>=0.23.0",
        "psutil",
        "tzlocal",
    ],
)

# cd "OneDrive - The Home Depot/Scripts/GitHub/da_gcp"
#
# python3 setup.py sdist
#
# twine check dist/da_gcp-2019.10.31.1.tar.gz
#
# twine upload --repository-url https://test.pypi.org/legacy/ dist/da_gcp-2019.10.31.1.tar.gz
#
# twine upload --repository pypi dist/da_gcp-2019.10.31.1.tar.gz
