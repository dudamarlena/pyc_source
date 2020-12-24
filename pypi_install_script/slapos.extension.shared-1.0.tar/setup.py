from setuptools import setup, find_packages
import os

version = '1.0'
name = 'slapos.extension.shared'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name=name,
    version=version,
    description="zc.buildout extension for SlapOS's shared feature.",
    long_description=(
        read('README.rst')
        + '\n' +
        read('CHANGELOG.rst')
        + '\n' +
        'Download\n'
        '***********************\n'
    ),
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='slapos shared',
    author='Yusei Tahara',
    author_email='yusei@nexedi.com',
    url='https://lab.nexedi.com/nexedi/slapos.extension.shared',
    license='GPLv3',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['slapos', 'slapos.extension'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'zc.buildout',
    ],
    entry_points = { 
        'zc.buildout.unloadextension': [
             'default = slapos.extension.shared:finish',
             ],
        },
)
