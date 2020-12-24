# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup


version = '0.1.0'

long_description = '\n'.join([
    open(os.path.join('README.rst')).read(),
    open(os.path.join('AUTHORS.rst')).read(),
    open(os.path.join('CHANGES.rst')).read(),
])

classifilers = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Framework :: Sphinx",
    "Framework :: Sphinx :: Extension",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Documentation",
    "Topic :: Documentation :: Sphinx",
    "Topic :: Text Processing :: Markup",
    "Topic :: Utilities",
]

setup(
    name='sphinxcontrib.mermaidjs',
    version=version,
    description="Sphinx extenstion to generate diagrams and flowcharts via Mermaid.js",
    long_description=long_description,
    classifiers=[],
    keywords=['sphinx', 'mermaidjs', 'visualization', 'chart', 'diagram'],
    author='Shoji KUMAGAI',
    author_email='take.this.2.your.grave@gmail.com',
    url='https://github.com/shkumagai/sphinxcontrib.mermaidjs',
    license='Apache License v2.0',
    namespace_packages=['sphinxcontrib'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'setuptools',
        'docutils',
        'sphinx', ],
    entry_points='''
        [sphinx_directives]
        setup = sphinxcontrib.mermaidjs:setup
    ''',
    zip_safe=False)
