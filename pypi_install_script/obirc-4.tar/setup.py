from setuptools import setup

def readme():
    with open('README') as file:
        return file.read()

setup(
    name='obirc',
    version='4',
    url='https://bitbucket.org/bthate/obirc',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="pure python3 IRC channel bot.",
    long_description=readme(),
    license='Public Domain',
    zip_safe=True,
    packages=["obirc", "ob"],
    scripts=["bin/obirc", "bin/obudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
