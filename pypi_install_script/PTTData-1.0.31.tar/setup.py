
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PTTData', 
    version='1.0.31', 
    description='Ptt Data', 
    long_description=long_description, 
    long_description_content_type='text/markdown',  
    url='https://github.com/linsamtw/PTTData',  
    author='linsam', 
    author_email='samlin266118@gmail.com', 
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='Ptt Data, python, text mining',
    packages=find_packages(exclude=['numpy', 'pymysql', 'pandas']),
    project_urls={
        'Source': 'https://github.com/linsamtw/PTTData',
    },
)
