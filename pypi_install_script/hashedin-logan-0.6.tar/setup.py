from distutils.core import setup

setup(
    name='hashedin-logan',
    version='0.6',
    author='Sripathi Krishnan',
    author_email='Sripathi@hashedin.com',
    packages=['logan'],
    scripts=[],
    url='http://pypi.python.org/pypi/Logan/',
    license='LICENSE',
    description='Python Logger plugin to send logs to Logan',
    long_description=open('README').read(),
    install_requires=[
        "certifi",
        "requests"
    ],
)