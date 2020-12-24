# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/glyphviewer/views.py
# Compiled at: 2018-03-17 23:16:32
import os, fnmatch, urlparse
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response
from django.conf import settings
from glyphviewer import glyphCatcher, glyphArray, GC_ERRORMSG
import random
from django.shortcuts import render
FONTS_DIR_ADD = 'glyphviewer/fonts/'
FIND_LOCAL_NAME = 0
FIND_LOCAL_RANDOM = 1
FIND_REMOTE = 2
localfontfiles = []
fontnametodirectory = {}
localfontempty = True

def doc(request):
    return render(request, 'glyphviewer/doc.html', {})


def getLocalFontFiles():
    """ Initialises localfontfiles to the list of fonts in the static directories,
        if there are any fonts to be found. This saves us reinitialising the
        same array.
    """
    global fontnametodirectory
    global localfontempty
    global localfontfiles
    if localfontfiles != []:
        localfontempty = False
        return (
         localfontfiles, fontnametodirectory)
    for i in [settings.STATIC_ROOT]:
        font_dir = os.path.join(i, FONTS_DIR_ADD)
        listdir = os.listdir(font_dir)
        filtereddir = filter(lambda x: fnmatch.fnmatch(x, '*.ttf') or fnmatch.fnmatch(x, '*.otf') or fnmatch.fnmatch(x, '*.woff') or fnmatch.fnmatch(x, '*.woff2'), listdir)
        for j in filtereddir:
            if not fontnametodirectory.has_key(j):
                localfontfiles.append(j)
                fontnametodirectory[j] = font_dir

    localfontfiles.sort()
    if localfontfiles != []:
        localfontempty = False
    else:
        localfontempty = True
    return (
     localfontfiles, fontnametodirectory)


def index(request):
    if 'shtables' not in request.GET:
        shtables = False
    else:
        shtables = True
    if 'blocks' not in request.GET:
        blocks = False
    else:
        blocks = True
    if 'Location' in request.GET:
        if request.GET['Location'] == 'Local':
            locchoice = FIND_LOCAL_NAME
        else:
            locchoice = FIND_REMOTE
    elif 'fonturl' in request.GET:
        locchoice = FIND_REMOTE
    else:
        locchoice = FIND_LOCAL_RANDOM
    fontlocal = request.GET.get('fontname', None)
    fontremote = request.GET.get('fonturl', None)
    localfontfiles, fontnametodirectory = getLocalFontFiles()
    localbase_url = urlparse.urljoin('http://' + request.META['HTTP_HOST'], settings.STATIC_URL)
    localfontdir_url = urlparse.urljoin(localbase_url, FONTS_DIR_ADD)
    if locchoice == FIND_LOCAL_NAME:
        is_remote = False
        chosenitem = fontlocal
        remoteurl = ''
        fetchpath = urlparse.urljoin(localfontdir_url, fontlocal)
        displayfont = fontlocal
        bCheckCORS = False
    elif locchoice == FIND_REMOTE:
        is_remote = True
        chosenitem = ''
        remoteurl = fontremote
        fetchpath = fontremote
        displayfont = fontremote
        bCheckCORS = True
    else:
        is_remote = False
        bCheckCORS = False
        random.seed()
        if len(localfontfiles):
            chosenitem = random.choice(localfontfiles)
        else:
            chosenitem = ''
        remoteurl = ''
        fetchpath = urlparse.urljoin(localfontdir_url, chosenitem)
        displayfont = chosenitem
    ourtuples = glyphCatcher(fetchpath, blocks, settings.DEBUG, bCheckCORS)
    ourerror = ourtuples[0]
    ourheader = ourtuples[1]
    ourglyphs = ourtuples[2]
    return render(request, 'glyphviewer/index.html', {'ourheader': ourheader, 'ourglyphs': ourglyphs, 
       'reslistdir': localfontfiles, 'chosenitem': chosenitem, 
       'displayfont': displayfont, 'blocks': blocks, 'ourerror': ourerror, 
       'ermsg': GC_ERRORMSG[ourerror], 'fontpath': fetchpath, 
       'shtables': shtables, 'remoteurl': remoteurl, 
       'is_remote': is_remote, 'localfontempty': localfontempty})