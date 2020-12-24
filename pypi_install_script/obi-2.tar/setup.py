from setuptools import setup

def readme():
    with open('README') as file:
        return file.read()

setup(
    name='obi',
    version='2',
    url='https://bitbucket.org/bthate/obi',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="OBI is a pure python3 IRC channel bot.",
    long_description=readme(),
    license='Public Domain',
    zip_safe=True,
    packages=["obi", "ob"],
    scripts=["bin/ob", "bin/obd", "bin/obi", "bin/obu", "bin/obl"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
