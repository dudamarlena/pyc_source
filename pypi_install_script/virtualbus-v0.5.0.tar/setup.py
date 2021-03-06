#!/usr/bin/env python3

from distutils.core import setup

from os import path

here = path.abspath(path.dirname(__file__))

################################################################################
try:
	# Git version when creating package
	import subprocess
	rv = subprocess.check_output(["git", "describe", "--always", "--dirty", "--long", "--tags"]).strip().decode()

	# Dirty repos are not allowed
	if "dirty" in rv:
		print("Repository is dirty... Try to clean it!")
		exit(0)

	label = rv.split("-")
	majorDotMinor = label[0]
	build = label[1]

	# Write version to a file for use inpackage management
	try:
		f = open(path.join(here, 'VERSION'), "w")
		f.write(majorDotMinor + "-" + build + "\n")
		f.close()
	except Exception:
			 pass
except Exception:
	# Version from file when installing
	try:
		f = open(path.join(here, 'VERSION'), "r")
		label = f.read()
		f.close()
		majorDotMinor = label[0]
		build = label[1]
	except Exception:
		print("Failed!")
		exit(1)
		#majorDotMinor = "v0.0"
		#build = "0"

version = majorDotMinor + "." + build
print("Version: {}".format(version))

################################################################################
# Long description
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


################################################################################
# Setup config
setup(
	name = 'virtualbus',
	packages = ['virtualbus'],
	version = version,
	license='MIT',
	description = 'Virtual bus',
	long_description = long_description,
	author = 'Kanelis Elias',
	author_email = 'hkanelhs@yahoo.gr',
	url = 'https://github.com/tedicreations/virtualbus',
	download_url = 'https://github.com/TediCreations/virtualbus/archive/' + str(majorDotMinor) + '.tar.gz',
	keywords = ['virtual', 'bus', 'socket', 'networking'],
	#install_requires=[],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
