try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import kosh


def readme_contents():
    with open("README.md") as f:
        return f.read()


setup(

    name='kosh',
    version=kosh.__version__,
    url='https://github.com/pshirali/kosh',
    description=kosh.__description__,
    long_description=readme_contents(),
    license='MIT License',

    author=kosh.__author__,
    author_email='praveengshirali@gmail.com',

    packages=['kosh'],
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),

)
