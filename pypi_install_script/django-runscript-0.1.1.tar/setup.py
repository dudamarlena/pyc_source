from distutils.core import setup

setup(
    name='django-runscript',
    packages=['django_runscript'],
    package_data={'django_runscript': ['management/commands/*.py']},
    version='0.1.1',
    license='MIT',
    description='Django command for running custom scripts with django environment.',
    author='retxxxirt',
    author_email='retxxirt@gmail.com',
    url='https://github.com/retxxxirt/django-runscript',
    keywords=['django runscript', 'django', 'django scripts', 'django management'],
    tests_require=(tests_require := ['django>=3.0,<3.1']),
    extras_require={'test': tests_require}
)
