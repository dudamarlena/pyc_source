#!/usr/bin/python
# -*- coding: utf-8 -*- 

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
#    der GNU General Public License, wie von der Free Software Foundation,
#    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren
#    veröffentlichten Version, weiterverbreiten und/oder modifizieren.
#
#    Dieses Programm wird in der Hoffnung, dass es nützlich sein wird, aber
#    OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
#    Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
#    Siehe die GNU General Public License für weitere Details.
#
#    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
#    Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.

import ax88179_178a_pinger_globals
from setuptools import setup, find_packages

setup(
    name = ax88179_178a_pinger_globals.app_name,
    version = ax88179_178a_pinger_globals.app_version_string,
    packages = ["."],
    install_requires = ["ping", "plac", ], 
    
    # metadata for upload to PyPI
    author = ax88179_178a_pinger_globals.app_author,
    author_email = ax88179_178a_pinger_globals.app_author_email,
    url=ax88179_178a_pinger_globals.app_website,
    description = "a helper to work around regular failure of the ax88179_178a driver for the ASIX A88179 and A88178 USB3.0-to-Gigabit-Ethernet adapters",
    license = "GPLv3",
    keywords = "chroot",
)

