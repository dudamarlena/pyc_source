from distutils.core import setup

setup(
    name='setify',
    packages=['setify'],
    version='0.3',
    license='MIT',
    description='Dataset packages',
    author='Mina Gabriel',
    author_email='developer.mina@gmail.com',
    url='https://github.com/MinaGabriel/setify.git',
    download_url='https://github.com/MinaGabriel/setify/archive/v0.3.tar.gz',
    keywords=['Dataset', 'Data'],
    install_requires=[
        'pandas',
        'numpy',
        'tqdm',
        'colorama'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
