import os

from setuptools import find_packages, setup


def prerelease_local_scheme(version):
    """Return local scheme version unless building on master in Gitlab.

    This function returns the local scheme version number
    (e.g. 0.0.0.dev<N>+g<HASH>) unless building on Gitlab for a
    pre-release in which case it ignores the hash and produces a
    PEP440 compliant pre-release version number (e.g. 0.0.0.dev<N>).

    """

    from setuptools_scm.version import get_local_node_and_date

    if 'CI_COMMIT_REF_NAME' in os.environ and \
       os.environ['CI_COMMIT_REF_NAME'] == 'master':
        return ''
    else:
        return get_local_node_and_date(version)


setup(
    name='stumpfwald',
    use_scm_version={'local_scheme': prerelease_local_scheme,
                     'root': '..',
                     'relative_to': __file__},
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    packages=find_packages(include=['stumpfwald']),
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'click>=7.0',
        'hvac',
        'mediainfo',
        'requests',
        'requests-toolbelt',
        'stumpf'
    ],
    entry_points={
        'console_scripts': [
            'stumpfwald=stumpfwald:cli'
        ]
    },
    license='Apache Software License 2.0',
)
