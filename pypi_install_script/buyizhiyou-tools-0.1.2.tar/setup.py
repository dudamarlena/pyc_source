# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='buyizhiyou-tools',
    version='0.1.2',
    description=(
        'some useful tools'
    ),
    long_description=open('README.rst').read(),
    author='buyizhiyou',
    author_email='2557040812@qq.com',
    maintainer='buyizhiyou',
    maintainer_email='2557040812@qq.com',
    license='BSD License',
    packages=['buyizhiyou'],
    platforms=["all"],
    url='https://github.com/buyizhiyou',
	install_requires=['six>=1.5.2',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
