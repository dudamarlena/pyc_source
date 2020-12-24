import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='lumber-cloud',
    version='0.0.4',
    license='MIT',
    author='InfiniteToken',
    author_email='infinitetoken@gmail.com',
    description='A Python package for cloud logging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/infinitetoken/Lumber-Python',
    download_url='https://github.com/infinitetoken/Lumber-Python/archive/0.0.4.tar.gz',
    keywords = ['LUMBER', 'LOGGING', 'LOG', 'CLOUD', 'OUTPUT'],
    packages=setuptools.find_packages(),
    install_requires=[ 'requests' ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
