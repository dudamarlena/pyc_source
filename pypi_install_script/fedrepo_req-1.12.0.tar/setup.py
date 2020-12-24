from setuptools import setup

description = \
    'A CLI tool to issue tickets for repo requests'

setup(
    author='Red Hat, Inc.',
    author_email='mprahl@redhat.com',
    data_files=[('/etc/fedrepo_req/', ['config.ini'])],
    description=description,
    entry_points='''
        [console_scripts]
        fedrepo-req=fedrepo_req.fedrepo_req:cli
        fedrepo-req-branch=fedrepo_req.fedrepo_req_branch:cli
        fedrepo-req-admin=fedrepo_req.fedrepo_req_admin:cli
    ''',
    include_package_data=True,
    install_requires=['click', 'python-bugzilla', 'python-fedora', 'pyyaml',
                      'requests', 'six'],
    license='GPLv2+',
    name='fedrepo_req',
    packages=['fedrepo_req'],
    package_dir={'fedrepo_req': 'fedrepo_req'},
    url='https://pagure.io/fedrepo_req',
    version='1.12.0',
)
