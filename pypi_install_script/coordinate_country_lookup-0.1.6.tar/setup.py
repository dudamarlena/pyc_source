from distutils.core import setup
setup(
  name = 'coordinate_country_lookup',         # How you named your package folder (MyLib)
  packages = ['coordinate_country_lookup'],   # Chose the same as "name"
  version = '0.1.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Returns the country of the latitude longitude tuple offline',   # Give a short description about your library
  author = 'Edward Brown',                   # Type in your name
  author_email = 'edward.j.e.brown@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/eddbrown/coodinate_country_lookup',   # Provide either the link to your github or to your website
  keywords = ['COORDINATE', 'COUNTRY', 'OFFLINE'],   # Keywords that define your package best
  install_requires=['shapely', 'geopandas'],
  package_data={'': ['countries/*']},
  include_package_data=True
)
