from setuptools import setup

setup(
    name='django-postgres-matviews-commands',
    version='2020.4.16',
    install_requires=[
        'Django',
        'setuptools',
    ],
    packages=[
        'django_postgres_matviews_commands',
        'django_postgres_matviews_commands.management',
        'django_postgres_matviews_commands.management.commands',
    ],
)
