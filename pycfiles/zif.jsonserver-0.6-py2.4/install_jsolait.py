# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/jsolait/install_jsolait.py
# Compiled at: 2007-05-25 16:54:17
import os, md5, urllib
loc = 'http://jsolait.net/download/'
filename = 'jsolait.2005-11-15.small.zip'
md5sum = 'c21c32a7a8756a35a0e48a30b710b3e1'
fileurl = loc + filename
for directory in ['src', 'doc', 'lib', 'libws']:
    if not os.path.exists(directory):
        os.mkdir(directory)

zippedfile = os.path.join('src', filename)
if not os.path.exists(zippedfile):
    print 'retrieving %s' % fileurl
    urllib.urlretrieve(fileurl, zippedfile)
else:
    print '%s exists; reprocessing. ' % zippedfile
    print 'to retrieve again, delete or rename %s.' % zippedfile
print 'checking md5'
filedata = file(zippedfile, 'r').read()
check = md5.new(filedata).hexdigest()
if not check == md5sum:
    raise ValueError('md5 sums do not match')
import zipfile
print 'unzipping %s' % zippedfile
zip = zipfile.ZipFile(zippedfile, 'r')
filesList = zip.namelist()
for k in filesList:
    if not k.endswith('/'):
        f = os.path.split(k)
        if 'doc' in f[0]:
            file(os.path.join('doc', f[1]), 'wb').write(zip.read(k))
        elif 'libws' in f[0]:
            file(os.path.join('libws', f[1]), 'wb').write(zip.read(k))
        elif 'lib' in f[0]:
            file(os.path.join('lib', f[1]), 'wb').write(zip.read(k))
        else:
            file(f[(-1)], 'wb').write(zip.read(k))

linesep = os.linesep
mfile = 'jsolait.js'
print 'patching %s' % mfile
t = file(mfile, 'U')
lines = t.readlines()
t.close()
t = file(mfile, 'w')
moda = False
modb = False
lineadded = False
for k in lines:
    d = k.rstrip()
    if d.find('mod.baseURI="./jsolait"') >= 0:
        s = 'mod.baseURI = "/++resource++jsolait";'
    elif d.find('baseURI)s') > 0:
        s = d.replace('/', '', 1)
        if lineadded == False:
            s = s + linesep + 'pythonkw:"%(baseURI)slib/pythonkw.js",'
            lineadded = True
    elif d.find('if(xmlhttp.status==200') == 0:
        s = 'if(xmlhttp.status==200||xmlhttp.status==0||xmlhttp.status==null){'
    else:
        s = d
    t.write('%s%s' % (s, linesep))

t.write('importModule=imprt' + linesep)
t.close()
t = file(mfile, 'r')
z = t.readlines()
t.close()
f = file('init.js', 'w')
for k in z:
    f.write(k)

f.close()
mfile = 'jsonrpc.js'
os.chdir('lib')
print 'patching %s' % mfile
t = file(mfile, 'U')
lines = t.readlines()
t.close()
t = file(mfile, 'w')
for k in lines:
    d = k.rstrip()
    if d.find('text/plain') >= 0:
        s = d.replace('text/plain', 'application/json-rpc')
    elif d.find('text/xml') >= 0:
        s = d.replace('text/xml', 'application/json-rpc')
    elif d.find('ImportFailed(') > 0 and not d.endswith(';'):
        s = d + ';'
    else:
        s = d
    t.write('%s%s' % (s, linesep))

t.close()
os.chdir('..')
print 'done.'
print 'original zip file is %s' % zippedfile