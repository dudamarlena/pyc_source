# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/+package+/public/moin_static/applets/FCKeditor/editor/filemanager/connectors/py/config.py
# Compiled at: 2010-02-28 10:28:47
"""
 * FCKeditor - The text editor for Internet - http://www.fckeditor.net
 * Copyright (C) 2003-2009 Frederico Caldeira Knabben
 *
 * == BEGIN LICENSE ==
 *
 * Licensed under the terms of any of the following licenses at your
 * choice:
 *
 *  - GNU General Public License Version 2 or later (the "GPL")
 *    http://www.gnu.org/licenses/gpl.html
 *
 *  - GNU Lesser General Public License Version 2.1 or later (the "LGPL")
 *    http://www.gnu.org/licenses/lgpl.html
 *
 *  - Mozilla Public License Version 1.1 or later (the "MPL")
 *    http://www.mozilla.org/MPL/MPL-1.1.html
 *
 * == END LICENSE ==
 *
 * Configuration file for the File Manager Connector for Python
"""
Enabled = False
UserFilesPath = '/userfiles/'
UserFilesAbsolutePath = ''
ForceSingleExtension = True
ConfigAllowedCommands = [
 'QuickUpload', 'FileUpload', 'GetFolders', 'GetFoldersAndFiles', 'CreateFolder']
ConfigAllowedTypes = [
 'File', 'Image', 'Flash', 'Media']
ChmodOnUpload = 493
ChmodOnFolderCreate = 493
AllowedExtensions = {}
DeniedExtensions = {}
FileTypesPath = {}
FileTypesAbsolutePath = {}
QuickUploadPath = {}
QuickUploadAbsolutePath = {}
AllowedExtensions['File'] = [
 '7z', 'aiff', 'asf', 'avi', 'bmp', 'csv', 'doc', 'fla', 'flv', 'gif', 'gz', 'gzip', 'jpeg', 'jpg', 'mid', 'mov', 'mp3', 'mp4', 'mpc', 'mpeg', 'mpg', 'ods', 'odt', 'pdf', 'png', 'ppt', 'pxd', 'qt', 'ram', 'rar', 'rm', 'rmi', 'rmvb', 'rtf', 'sdc', 'sitd', 'swf', 'sxc', 'sxw', 'tar', 'tgz', 'tif', 'tiff', 'txt', 'vsd', 'wav', 'wma', 'wmv', 'xls', 'xml', 'zip']
DeniedExtensions['File'] = []
FileTypesPath['File'] = UserFilesPath + 'file/'
FileTypesAbsolutePath['File'] = not UserFilesAbsolutePath == '' and UserFilesAbsolutePath + 'file/' or ''
QuickUploadPath['File'] = FileTypesPath['File']
QuickUploadAbsolutePath['File'] = FileTypesAbsolutePath['File']
AllowedExtensions['Image'] = [
 'bmp', 'gif', 'jpeg', 'jpg', 'png']
DeniedExtensions['Image'] = []
FileTypesPath['Image'] = UserFilesPath + 'image/'
FileTypesAbsolutePath['Image'] = not UserFilesAbsolutePath == '' and UserFilesAbsolutePath + 'image/' or ''
QuickUploadPath['Image'] = FileTypesPath['Image']
QuickUploadAbsolutePath['Image'] = FileTypesAbsolutePath['Image']
AllowedExtensions['Flash'] = [
 'swf', 'flv']
DeniedExtensions['Flash'] = []
FileTypesPath['Flash'] = UserFilesPath + 'flash/'
FileTypesAbsolutePath['Flash'] = not UserFilesAbsolutePath == '' and UserFilesAbsolutePath + 'flash/' or ''
QuickUploadPath['Flash'] = FileTypesPath['Flash']
QuickUploadAbsolutePath['Flash'] = FileTypesAbsolutePath['Flash']
AllowedExtensions['Media'] = [
 'aiff', 'asf', 'avi', 'bmp', 'fla', 'flv', 'gif', 'jpeg', 'jpg', 'mid', 'mov', 'mp3', 'mp4', 'mpc', 'mpeg', 'mpg', 'png', 'qt', 'ram', 'rm', 'rmi', 'rmvb', 'swf', 'tif', 'tiff', 'wav', 'wma', 'wmv']
DeniedExtensions['Media'] = []
FileTypesPath['Media'] = UserFilesPath + 'media/'
FileTypesAbsolutePath['Media'] = not UserFilesAbsolutePath == '' and UserFilesAbsolutePath + 'media/' or ''
QuickUploadPath['Media'] = FileTypesPath['Media']
QuickUploadAbsolutePath['Media'] = FileTypesAbsolutePath['Media']