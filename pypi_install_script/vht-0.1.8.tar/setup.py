#!/usr/bin/env python3

from setuptools import setup, Extension

setup(name = "vht",
	version = "0.1.8",
	description = "Valhalla MIDI Tracker",
	author = "Remigiusz Dybka",
	author_email = "remigiusz.dybka@gmail.com",
	url = "https://github.com/rdybka/vht",
	license = 'GPLv3+',
	ext_modules = [Extension("_libcvht", ["libvht/libvht.c",
			"libvht/libvht_wrap.c",
			"libvht/jack_client.c",
			"libvht/jack_process.c",
			"libvht/midi_event.c",
			"libvht/module.c",
			"libvht/row.c",
			"libvht/ctrlrow.c",
			"libvht/sequence.c",
			"libvht/track.c",
			"libvht/envelope.c",], 
			libraries = ["jack"])],

	packages = ["vht", "libvht"],
	entry_points={
        'console_scripts': [
            'vht = vht.main:run',
        ]},
	
	data_files = [
		('share/vht', ['data/vht.svg', 'data/menu.ui']),
		('share/icons', ['data/vht.svg']),
		('share/applications', ['data/com.github.rdybka.vht.desktop'])
	],
	
	classifiers=[
		'Environment :: X11 Applications :: Gnome',
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Programming Language :: Python :: 3',
		'Programming Language :: C',
		'Topic :: Multimedia :: Sound/Audio :: MIDI'
	]
)
