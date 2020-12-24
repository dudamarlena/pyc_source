
import setuptools


setuptools.setup(setup_requires=['pbr'],
                 pbr=True,
                 test_suite="pylint_oca.test",
                 package_data={'': ['*.yaml']})
