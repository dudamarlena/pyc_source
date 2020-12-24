from distutils.core import setup

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session='hack')

reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='adsm',
    version='2.1.0',
    author='Parmentier Laurent',
    author_email='laurent.parmentier@corp.ovh.com',
    packages=['adsm', 'adsm.backend', 'adsm.extractor'],
    scripts=['bin/adsm'],
    url='https://gitlab.society-lbl.com/thesis/dsm',
    description='Another Data Set Manager (ADSM)',
    install_requires=reqs,
    include_package_data=True,
    package_data={'adsm': ['default.yaml']}
)
