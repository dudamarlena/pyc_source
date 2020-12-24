from setuptools import setup
from turing_machine_executor import __version__ as version

with open("README.md", "r") as f:
    long_description = f.read()
    f.close()

setup(
    name="turing_machine_executor",
    version=version,
    description="A Turing Machine executor",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Andrea Esposito',
    author_email='esposito_andrea99@hotmail.com',
    url="https://github.com/espositoandrea/Turing-Machine-Executor",
    packages=['turing_machine_executor'],
    download_url='https://github.com/espositoandrea/Turing-Machine-Executor/archive/v1.1.0-alpha.tar.gz',
    keywords=['Turing', 'Machine', 'Executor', 'EMT'],
    install_requires=["colorama", "pyfiglet"],
    entry_points={
        'console_scripts': [
            'emt = turing_machine_executor.__main__:run',
            'turing-machine-executor = turing_machine_executor.__main__:run',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
