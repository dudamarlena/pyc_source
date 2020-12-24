from distutils.core import setup
setup(
  name = 'chronopost-python-sdk',         # How you named your package folder (MyLib)
  packages = ['chronopost_python_sdk'],   # Chose the same as "name"
  version = '1.0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python SDK for Chronopost',   # Give a short description about your library
  author = 'Andre Rosado',                   # Type in your name
  author_email = 'rosado_andre@live.com.pt',      # Type in your E-Mail
  url = 'https://github.com/afbrosado',   # Provide either the link to your github or to your website
  keywords = ['Chronopost', 'Gateway'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'zeep',
          'requests',
          'xmltodict'
      ],
  classifiers=[
  ],
)
