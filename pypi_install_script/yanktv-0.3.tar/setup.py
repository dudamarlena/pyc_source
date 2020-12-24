
from setuptools import setup, find_packages

from yanktv import __version__

setup(
    name='yanktv',
    version=__version__,
    description='Yank torrents for the latest episodes of your tv shows.',
    long_description=open('README.rst').read(),
    keywords='tv show torrent episodes',
    url='https://github.com/lmas/yanktv',
    download_url='https://github.com/lmas/yanktv/releases',
    author='A. Svensson',
    author_email='lmasvensson@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pyxdg',
    ],
    scripts=['bin/yanktv'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[ # See: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Communications :: File Sharing',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities',
    ],
)

