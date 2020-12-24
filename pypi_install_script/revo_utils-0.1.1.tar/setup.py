from setuptools import setup, find_packages

setup(
    name="revo_utils",
    version='0.1.1',
    packages=find_packages(),
    license='gpl-3.0',
    description='A collection of utilities which we use in all our projects',
    author='Robert Binneman',
    author_email='r.binneman@gmail.com',
    url='https://github.com/RobertBinneman/revo_utils/',
    download_url='https://github.com/RobertBinneman/revo_utils/archive/0.1.1.tar.gz',
    keywords=['UTILITIES'],
    install_requires=[
        'cryptography',
        'djangorestframework',
        'django',
        'python-dateutil'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
