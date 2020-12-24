from setuptools import setup


with open('README.md') as fp:
    long_description = fp.read()


setup(
    name='datapype',
    version='0.0.1',
    author='Adam Johnston',
    author_email='amj69@case.edu',
    description='Proof of concept pipeline framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/a-johnston/datapype',
    packages=['datapype'],
    install_requires=[
        'pyrsistent',
    ],
    license=['MIT'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
