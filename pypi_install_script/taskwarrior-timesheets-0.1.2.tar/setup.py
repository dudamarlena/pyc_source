from setuptools import setup, find_packages

setup(name='taskwarrior-timesheets',
      version='0.1.2',
      description='Time tracking for Task Warrior, connects to the Tempo Timesheets plugin in JIRA',
      url='http://git@stash.t.is:7999/san/taskwarrior-timesheets.git',
      author='Eric Nielsen',
      author_email='ericn@tmsoftware.is',
      packages=find_packages(),
      install_requires=[
        'GitPython==0.3.2.1',
        'argparse==1.2.1',
        'cement==2.4.0',
        'gitdb==0.6.0',
        'iso8601==0.1.10',
        'jira==0.32',
        'lscolumns==0.1.0',
        'oauthlib==0.7.2',
        'prettytable==0.7.2',
        'py-dateutil==2.2',
        'python-dateutil==2.2',
        'pytz==2014.9',
        'requests==2.5.0',
        'requests-oauthlib==0.4.2',
        'six==1.8.0',
        'smmap==0.8.3',
        'taskw==0.8.6',
        'tempo==0.1',
        'tlslite==0.4.8',
        'wsgiref==0.1.2',
        'xmltodict==0.9.0',
      ],
      entry_points={
        'console_scripts': [
            'taskwarrior_timesheets = taskwarrior_timesheets:main'
        ]
      },
)
