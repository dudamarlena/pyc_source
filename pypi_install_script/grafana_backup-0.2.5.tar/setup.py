from setuptools import setup

setup(name='grafana_backup',
      version='0.2.5',
      description='Backup grafana using the API',
      url='https://github.com/opentable/grafana_backup',
      author='Carl Flippin',
      author_email='cflippin@opentable.com',
      license='MIT',
      packages=['grafana_backup'],
      install_requires=[
          'requests'
      ],
      entry_points = {
          'console_scripts': ['grafana_backup=grafana_backup.__main__:main']
      })
