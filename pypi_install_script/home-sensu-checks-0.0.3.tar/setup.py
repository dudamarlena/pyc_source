from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='home-sensu-checks',
    version='0.0.3',
    author='Erik Reid',
    author_email='merikreid@gmail.com',
    description='Custom checks/metrics for use with Sensu',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=('https://github.com/susrik/home_sensu_checks'),
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta'
    ],
    python_requires='>=3.6',
    install_requires=[
        'click',
        'fritzconnection',
    ],
    entry_points = {
        'console_scripts': [
            'fritz-metrics=home_sensu_checks.fritz:cli',
        ]
    }
)
