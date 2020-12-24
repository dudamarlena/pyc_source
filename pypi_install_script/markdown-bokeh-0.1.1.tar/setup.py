from setuptools import setup, find_packages
from os import path

setup(
    name='markdown-bokeh',
    packages=find_packages(),
    version='0.1.1',
    description='This is an extension to Python-Markdown which provides the ability to include plots from bokeh.',
    author='Caleb Fangmeier',
    author_email='caleb@fangmeier.tech',
    url='https://github.com/cfangmeier/markdown-bokeh/',
    keywords=['Markdown', 'typesetting', 'bokeh', 'plugin', 'extension'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['markdown']
)
