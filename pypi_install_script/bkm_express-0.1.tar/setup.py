from distutils.core import setup

setup(
    name='bkm_express',
    packages=['bkm_express'],
    version='0.1',
    license='MIT',
    description='This repository includes BKM expres client for python',
    author='KAAN ANT',
    author_email='kaanantt@gmail.com',
    url='https://github.com/kaanant',
    keywords=['Pyton', 'Payment', 'BkmExpress', 'Client'],
    install_requires=[
        'pycrypto',
        'Crypto',
        'requests',
        'mock',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
)
