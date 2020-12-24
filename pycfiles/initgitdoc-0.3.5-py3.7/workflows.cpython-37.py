# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/templates/workflows.py
# Compiled at: 2020-04-22 18:07:54
# Size of source mod 2**32: 889 bytes
pypi_workflow = "\n# This workflows will upload a Python Package using Twine when a release is created\n# For more information see: https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions#publishing-to-package-registries\n\nname: Upload Python Package\n\non:\n  release:\n    types: [created]\n\njobs:\n  deploy:\n\n    runs-on: ubuntu-latest\n\n    steps:\n    - uses: actions/checkout@v2\n    - name: Set up Python\n      uses: actions/setup-python@v1\n      with:\n        python-version: '3.x'\n    - name: Install dependencies\n      run: |\n        python -m pip install --upgrade pip\n        pip install setuptools wheel twine\n    - name: Build and publish\n      env:\n        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}\n        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}\n      run: |\n        python setup.py sdist bdist_wheel\n        twine upload dist/*\n"