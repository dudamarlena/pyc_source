from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", 'r') as rqtxt:
    requirements = rqtxt.readlines()
    
setup(
    name="random-open-port",
    version="0.0.3",
    description="A simple command line tool for generating a random non-affiliated port.",
    author="Joe Habel",
    author_email="habeljw@gmail.com",
    packages=['random_open_port',],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/joe-habel/random-open-port.git",
    install_requires=requirements,
    python_requires='>=3',
    entry_points = {
        'console_scripts' : [
            'random-port = random_open_port.random_open_port:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
