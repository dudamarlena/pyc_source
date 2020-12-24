from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='pygns3-elsholz',
    version='3.11',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Software Development :: Libraries',
                 ],
    packages=['pygns3', ],
    url='https://github.com/elsholz/PyGNS3',
    license='MIT',
    author='elsholz',
    author_email='maarten@vanderwoord.nl',
    install_requires=['requests', ],
    description='Python implementation of the GNS3 API. Fork by elsholz from mvdwoord/PyGNS3',
    long_description=readme(),
)
