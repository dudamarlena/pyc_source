
from distutils.core import setup

setup(
    name = 'sugarpill',
    packages = ['sugarpill'],
    version = '0.0.0',
    license='MIT',
    description = '🍬 Distributed Randomised Control Trials',
    keywords = ['statistics', 'dashboard', 'distributed', 'multiprocessing', 'multithreading', 'cluster', 'experiments', 'scheduler', 'logger'],

    author = 'Nathan Michlo',
    author_email = 'NathanJMichlo@gmail.com',

    url = 'https://github.com/nmichlo/sugarpill',
    # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',

    install_requires=[],

    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)