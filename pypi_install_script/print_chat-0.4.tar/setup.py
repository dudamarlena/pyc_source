from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='print_chat',
    version='0.4',
    packages=find_packages(),
    description='Small print tool for implementing chat in the terminal',
    long_description=readme(),
    author='IVIGOR13',
    author_email='igor.i.v.a.13@gmail.com',
    url='https://github.com/IVIGOR13/print_chat',
    download_url='https://github.com/IVIGOR13/print_chat/archive/0.4.tar.gz',
    keywords=['chat', 'terminal'],
    python_requires='>=3',
    include_package_data=True,
    license='MIT',
    install_requires=[
    	'termcolor',
    	'colorama'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Terminals'
    ]
)
