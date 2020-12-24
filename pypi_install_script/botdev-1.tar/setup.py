# setup.py

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botdev',
    version='1',
    url='https://bitbucket.org/botlib/botdev',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" BOTDEV is the development of BOTLIB. """,
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    install_requires=["libobj", "botlib", "botd"],
    packages=["botdev"],
    scripts=["bin/bclone", "bin/bcreate"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
