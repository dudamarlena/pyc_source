from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mosenergosbyt',
    packages=['mosenergosbyt'],
    version='0.1.5',
    license='MIT',
    description='api для работы с порталом мосэнергосбыт',
    long_description=long_description,
    author='@kkuryshev',
    author_email='kkurishev@gmail.com',
    url='https://github.com/kkuryshev/mosenergosbyt',
    download_url='https://github.com/kkuryshev/mosenergosbyt/archive/pypi-0_1.tar.gz',
    keywords=['mosenergosbyt', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=[
        'requests'
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
