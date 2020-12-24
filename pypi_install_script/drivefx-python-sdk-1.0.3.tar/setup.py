from distutils.core import setup
setup(
  name = 'drivefx-python-sdk',         # How you named your package folder (MyLib)
  packages = ['drivefx_python_sdk'],   # Chose the same as "name"
  version = '1.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python SDK for DriveFX',   # Give a short description about your library
  author = 'Marco Mendao',                   # Type in your name
  author_email = 'mac.mendao@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Menda0',   # Provide either the link to your github or to your website
  keywords = ['DriveFx', 'Invoice', 'Stocks', 'Logistics', 'Integration'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'request'
      ],
  classifiers=[
  ],
)
