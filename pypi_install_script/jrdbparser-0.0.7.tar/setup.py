from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='jrdbparser',
    version='0.0.7',
    description='Parser for JRDB data',
    long_description=readme,
    author='Kanta Kuramoto',
    author_email='kanta208@gmail.com',
    url='https://github.com/otomarukanta/jrdbparser',
    license=license,
    packages=find_packages(exclude=('tests')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)
