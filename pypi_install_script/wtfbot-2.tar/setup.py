from setuptools import setup

def readme():
    with open('README') as file:
        return file.read()

setup(
    name='wtfbot',
    version='2',
    url='https://bitbucket.org/bthate/wtfbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="a pure python3 IRC channel bot.",
    long_description=readme(),
    license='Public Domain',
    zip_safe=True,
    packages=["wtf"],
    scripts=["bin/wtfbot", "bin/wtfudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
