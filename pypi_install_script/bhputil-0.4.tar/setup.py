from setuptools import setup

setup(
    name='bhputil',
    url='https://github.com/dmparker0/bhputil/',
    author='Daniel McCracken',
    author_email='mccrackend@boulderhousing.org',
    packages=['bhputil'],
    install_requires=['xlwings','pandas','pyodbc','selenium','pywin32'],
    version='0.4',
    license='MIT',
    description='Utility functions for BHP process automation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    download_url = 'https://github.com/dmparker0/bhputil/archive/v0.4.tar.gz', 
)
