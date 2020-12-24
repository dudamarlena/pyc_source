import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#     CHANGES = f.read()
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = [
    'requests>=2.18.4',
    'urllib3>=1.22',
    'chardet>=3.0.4',
    'certifi>=2018.1.18',
    'idna>=2.6',
    'configparser>=3.5.0',
    'setuptools>=39.0.1'
]
setup(name='kosihubpublisher',
      version='0.0.1',
      description='A tool to update information on KOSi Hub',
      # long_description=README + '\n\n' + CHANGES,
      long_description=read('README.md'),
      # classifiers=[
      #     "Programming Language :: Python -3.6",
      #     "Framework :: ",
      #     "Topic :: Internet :: WWW/HTTP",
      #     "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      # ],
      author='yueha002',
      author_email='yue.ha@keysight.com',
      url='https://bitbucket.it.keysight.com/scm/fus/kosihubpublisher_repo.git',
      keywords='KOSi python',
      python_requires='>=3',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='Test',
      install_requires=requires,
      package_data={  # Optional
          # 'Helper':['KOSiHubPublisher/Helper'],
          # 'Options': ['KOSiHubPublisher/Options'],
          'profile': ['kosihubpublisher/profile.json'],
          # 'template': ['KOSiHubPublisher/request.json'],
          '': ['README.md'],
          'setting': ['kosihubpublisher/setting.conf']
      },
      entry_points={
          'console_scripts':[
              'kosihubpublisher = kosihubpublisher.main:main'
          ]
      },
      # """\
      # [paste.app_factory]
      # main = mypackage:main
      # [console_scripts]
      # initialize_mypackage_db = mypackage.scripts.initializedb:main
      # """,

      )