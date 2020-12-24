from distutils.core import setup

setup(
    name='RankBasedMonteCarlo',
    version='0.1.3',
    packages=['RankBasedMonteCarlo',],
    license='MIT',
    install_requires=[
        'numpy',
        'pandas'
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
    keywords = ['Monte Carlo', 'Rank based', 'Statistics'],
    url = 'https://github.com/tazzben/RankBasedMonteCarlo',
    download_url = 'https://github.com/tazzben/RankBasedMonteCarlo/archive/v0.1.3.tar.gz',  
    description = 'A set of Monte Carlo based tools to create test statistics for four non-parametric rank-based tests: Mann-Whitney (MW), Kruskal-Wallis (KW), Kolmogorov-Smirnov (KS) and Kuiper (K).'
)
