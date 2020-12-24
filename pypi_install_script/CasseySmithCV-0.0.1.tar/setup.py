from distutils.core import setup

setup(
    name='CasseySmithCV',
    version='0.0.1',
    packages=['CasseySmithCV',],
    license='MIT',
    install_requires=[
        'numpy',
        'pandas',
        'progress'
    ],
    author='Ben Smith',
    author_email='bosmith@unomaha.edu',
    classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Science/Research', 
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    ],
    keywords = ['Monte Carlo', 'EG Statistic', 'Statistics'],
    url = 'https://github.com/tazzben/CasseySmithCV',
    download_url = 'https://github.com/tazzben/CasseySmithCV/archive/v0.0.1.tar.gz',  
    description = 'Produces critical values using the methods described in Cassey Smith (2014).  Code is modernized from version published with paper to take advantage of advances in computing.'
)
