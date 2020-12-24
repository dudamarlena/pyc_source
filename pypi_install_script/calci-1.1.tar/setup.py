from setuptools import setup

setup(
    name = 'calci',
    version = 1.1,
    long_description=open('README.txt').read(),
    author='ganesh',
    author_email='ganesh@server.com',
    url="http://www.foopackage.com/",
    packages=['calci'],
    #install_requires=['flask', 'flask-restful'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
