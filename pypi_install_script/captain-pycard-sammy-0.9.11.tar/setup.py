from setuptools import setup, find_packages


# Calculate the version based on pycard.VERSION
version = '.'.join([str(v) for v in __import__('pycard').VERSION])

setup(
    name='captain-pycard-sammy',
    description='A simple library for payment card validation',
    version=version,
    author='Sammy',
    author_email='sammy.teillet@gmail.com',
    url='https://github.com/Samox/pycard.git',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Topic :: Utilities'
    ],
    packages=find_packages(),
)
