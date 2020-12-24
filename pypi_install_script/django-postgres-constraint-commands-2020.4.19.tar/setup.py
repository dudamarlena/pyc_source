from setuptools import setup

setup(
    name='django-postgres-constraint-commands',
    version='2020.4.19',
    install_requires=[
        'Django',
        'setuptools',
    ],
    packages=[
        'django_postgres_constraint_commands',
        'django_postgres_constraint_commands.management',
        'django_postgres_constraint_commands.management.commands',
    ],
)
