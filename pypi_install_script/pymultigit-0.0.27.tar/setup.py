import setuptools

setuptools.setup(
    name='pymultigit',
    version='0.0.27',
    description='pymultigit is a command to help you deal with multiple git repositories',
    long_description='this is the long description of pymultigit',
    url='https://veltzer.github.io/pymultigit',
    download_url='https://github.com/veltzer/pymultigit',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='git python repositories multiple',
    packages=setuptools.find_packages(),
    install_requires=[
        'click',
        'gitpython',
        'pyfakeuse',
    ],
    entry_points={
        'console_scripts': [
            'pymultigit=pymultigit.mg:cli',
        ],
    },
)
