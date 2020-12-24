from setuptools import setup

setup(
    name = 'coutils',
    packages = ['coutils'],
    version = '0.1.2',
    license='MIT',
    description = 'common code for utils',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author = 'Paul Singman',
    author_email = 'paul.singman@equinox.com',
    url = 'https://github.com/equinoxfitness/datacoco.utils',
    download_url = 'https://github.com/equinoxfitness/datacoco.util/archive/0.1.tar.gz',
    keywords = ['email tools', 'ftp tools'],   # Keywords that define your package best
    install_requires=[
        'pysftp==0.2.9',
        'boto3==1.9.203',
        'botocore>1.9.0'
    ]
)
