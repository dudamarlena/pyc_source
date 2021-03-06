from setuptools import setup


setup(
    name='grapher-core',
    version='2.0.9',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['data', 'visualization', 'monitoring', 'graphs'],
    python_requires='~=3.7',
    description='Grapher core server and libraries',
    author='Volodymyr Paslavskyy',
    author_email='qfoxic@gmail.com',
    packages=['grapher.core'],
    install_requires=['websockets==8.1'],
    url='https://gitlab.com/grapher/grapher-core/',
    download_url='https://gitlab.com/grapher/grapher-core/-/archive/2.0.9/grapher-core-2.0.9.tar.gz'
)
