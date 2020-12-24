from setuptools import setup, find_packages
import os
# https://stackoverflow.com/questions/49689880/proper-way-to-parse-requirements-file-after-pip-upgrade-to-pip-10-x-x
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'default.txt'), session=PipSession())


setup(
    name='micro-ussd-airflow-engine',
    version="0.1.2",
    packages=find_packages(exclude=('ussd_engine',)),
    url='https://github.com/seidu626/ussd_engine',
    install_requires=[str(requirement.req) for requirement in requirements],
    include_package_data=True,
    license='MIT',
    author='Seidu',
    author_email='seidu.abdulai@hotmail.com',
    description='Micro Ussd Engine Airflow Library',
    # I explain this later on
    download_url='https://github.com/seidu626/ussd_engine/archive/v0.1.tar.gz',
    keywords=['USSD', 'GATEWAY'],   # Keywords that define your package best
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
