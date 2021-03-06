
from setuptools import setup
setup(**{'author': 'puntonim',
 'author_email': 'foo@gmail.com',
 'classifiers': ['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Internet :: WWW/HTTP'],
 'description': 'Flower service client',
 'include_package_data': True,
 'install_requires': ['pkgsettings<1,>=0.12.0', 'requests<3,>=2.19.1'],
 'long_description': "[![Build Status](https://travis-ci.org/puntonim/service-flower.svg?branch=master)](https://travis-ci.org/puntonim/service-flower)\n\n# Flower service client\n\nThis package is service client for Flower API used to monitor Celery.\n\n## Client usage\n\n```python\n# Configure settings.\nimport service_flower.conf\nd = dict(\n    BASE_URL='https://inspire-qa-worker3-task1.cern.ch/api',\n    REQUEST_TIMEOUT=30,\n    HTTP_AUTH_USERNAME='user',\n    HTTP_AUTH_PASSWORD='pass',\n)\nservice_flower.conf.settings.configure(**d)\n\n# Use the client.\nfrom service_flower.client import FlowerClient\nclient = FlowerClient()\nresponse = client.get_workers(workername='celery@inspire-qa-worker3-task5.cern.ch')\nresponse.raise_for_result()\nqueues = response.get_active_queues_names('celery@inspire-qa-worker3-task5.cern.ch')\n```\n\n## Development\n\n```bash\n# Create a venv and install the requirements:\n$ make venv\n\n# Run isort and lint:\n$ make isort\n$ make lint\n\n# Run all the tests:\n$ make test  # tox against Python27 and Python36.\n$ tox -e py27  # tox against a specific Python version.\n$ pytest  # pytest against the active venv.\n\n# Run a specific test:\n$ make test/tests/test_client.py  # tox against Python27 and Python36.\n$ tox -e py27 -- tests/test_client.py  # tox against a specific Python version.\n$ pytest tests/test_client.py  # pytest against the active venv.\n```\n\nTo publish on PyPi, first set the PyPi credentials:\n\n```bash\n# Edit .pypirc:\n$ cat $HOME/.pypirc\n[pypi]\nusername: myuser\npassword: mypass\n```\n\n```bash\n# Edit the version in `setup_gen.py`.\n# ... version=pep440_version('1.1.1'),\n# Then generate setup.py with:\n$ make setup.py\n# Commit, tag, push:\n$ git commit -m '1.1.1 release'\n$ git tag 1.1.1\n$ git push origin master --tags\n\n# Finally publish:\n$ make publish\n```\n",
 'name': 'service-flower',
 'packages': ['service_flower'],
 'tests_require': ['tox'],
 'url': 'https://github.com/puntonim/service-flower',
 'version': '1.0.1',
 'zip_safe': False})
