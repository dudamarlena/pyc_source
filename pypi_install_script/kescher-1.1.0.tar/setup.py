from setuptools import find_packages, setup

from kescher import __version__

setup(
    name='kescher',
    version=__version__,
    description=('Framework for Caching with django'),
    long_description=open('README.rst').read(),
    author='puzzle & play GmbH',
    author_email='scrum@puzzleandplay.de',
    url='https://www.fotopuzzle.de/',
    license='AGPLv3',
    platforms=['any'],
    packages=find_packages(exclude=['tests']),
    package_data={},
    include_package_data=True,
    install_requires=[
        'django>=2.0,<3.0',
        'papyru>=0.0.1.dev38',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    test_suite='tests.settings.run',
)
