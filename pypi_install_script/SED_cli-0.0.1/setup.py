from distutils.core import setup
setup(
    name='SED_cli',
    packages=['.'],
    version='0.0.1',
    license='MIT',
    description='This package is intended to help configuring and developing of embedded projects - It will not compile, or check or do anything \
        besides configuration. The goal is to provided a way to developer simply program what he/she wants and let the package deal with all the configuration needed.',
    author='Victor Hugo Belinello',
    author_email='victorbelinello17@gmail.com',
    url='https://github.com/belinello/SED_cli',
    download_url='https://github.com/belinello/SED_cli/archive/v0.0.1-alpha.tar.gz',
    keywords=['Embedded', 'Configuration'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
