# from distutils.core import setup
import setuptools
import folder_organizer

setuptools.setup(
  name = 'folder-organizer',
  packages = [
    'folder_organizer',
    'folder_organizer.utils',
    'folder_organizer.interfaces',
    'folder_organizer.resources'
  ],
  version = '1.1',
  description = 'A simple folder organizer',
  author = 'Unai Minaberry y Avelino Navarro',
  author_email = 'unihernandez22@yahoo.com',
  url = 'https://github.com/unihernandez22/folder-organizer',
  download_url = 'https://github.com/unihernandez22/folder-organizer/tarball/0.1',
  keywords = ['organize', 'folders', 'files'],
  data_files = [('folder-organizer-resources', ['folder_organizer/resources/data.json', 'folder_organizer/resources/folder'])],
  install_requires=[
      'pyqt5',
  ],
  entry_points = {
        'console_scripts': [
            'folder-organizer=folder_organizer.open:main'
        ]
	}
)