from distutils.core import setup
import os
os.system("rm -rf dist")
setup(
  name = 'TAFA',         # How you named your package folder (MyLib)
  packages = ['tafa'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'simple module for facebook',   # Give a short description about your library
  long_description = """
import tafa
ses = tafa.Account(facebook_cookies)
print(ses.name)
print(ses.id)
""",
  author = 'SalisM3',                   # Type in your name
  author_email = 'salism3.server@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/salismazaya/fbparser',   # Provide either the link to your github or to your website
  keywords = ['facebook', 'python', 'tools'],   # Keywords that define your package best
  install_requires=['urllib3','bs4'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
  ],
)
os.system("twine upload dist/*")
