from distutils.core import setup
setup(
  name = 'jugaad-trader',         # How you named your package folder (MyLib)
  packages = ['jugaad_trader'],   # Chose the same as "name"
  install_requires=[            # I get to this in a second
      "requests==2.23.0"
      ],
  
)
