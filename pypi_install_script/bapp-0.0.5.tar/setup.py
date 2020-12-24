from setuptools import setup

setup(
    name='bapp',
    packages=['bapp'],
    version='0.0.5',
    description='Python API Client for BAPP',
    author='Cristian Boboc',
    author_email='cristi@cbsoft.ro',
    url='https://github.com/bapp-open/bapp-python',
    license='GPL',
    download_url='https://github.com/bapp-open/bapp-python/archive/master.zip',
    keywords=['bapp'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
