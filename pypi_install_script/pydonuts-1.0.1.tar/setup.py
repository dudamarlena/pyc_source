from setuptools import setup
from os.path import join, abspath, dirname

this_directory = abspath(dirname(__file__))

with open(join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pydonuts',
    version='1.0.1',
    description='Library for work with VK Donuts app.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GNU General Public License v3 (GPLv3)',
    packages=['pydonuts'],
    author='Gr4Yka',
    author_email='greywolf2428@gmail.com',
    url='https://github.com/Gr4Yka/pydonuts',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['importlib', 'requests'],
    keywords = ['pydonuts']
)
