from setuptools import setup
from io import open

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CodingToolBox',
    version='1.2.1',
    description='Tools for coding.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kent010341/CodingToolBox',
    author='Kent010341',
    author_email='kent010341@gmail.com',
    install_requires=['numpy', 'matplotlib'],
    license='MIT',
    packages=['CodingToolBox'],
    zip_safe=False,
    keywords='coding programming animated algorithm',
    classifiers=[
    	'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    python_requires='>=3.6'
)