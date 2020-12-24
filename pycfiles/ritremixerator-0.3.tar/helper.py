# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eitan/Documents/code/RITRemixerator/dorrie/../dorrie/comps/helper.py
# Compiled at: 2012-02-01 17:21:04
import os
from django.conf import settings
from models import Spin, Group, Package

def get_spin(id):
    """
    return Spin object from id
    """
    return Spin.objects.get(id=id)


def new_spin(name, base_ks, uploaded):
    """
    Return new spin
    """
    spin = Spin(name=name, baseks=base_ks, uploaded=uploaded)
    spin.save()
    return spin


def add_lang_tz(spin_id, lang, tz):
    """
    Add language and timezone
    """
    spin = get_spin(spin_id)
    spin.language = lang
    spin.timezone = tz
    spin.save()
    return spin


def package(name):
    """
    New or existing package
    """
    try:
        package = Package.objects.get(name__exact=name)
    except:
        package = Package(name=name)
        package.save()

    return package


def group(name):
    """
    New or existing group
    """
    try:
        group = Group.objects.get(name__exact=name)
    except:
        group = Group(name=name)
        group.save()

    return group


def add_rem_groups(spin, type, string):
    """
    $function_name
    """
    if string:
        g = group(string)
    else:
        return
    if type == '+':
        if g in spin.gminus.all():
            spin.gminus.remove(g)
        elif g not in spin.gplus.all():
            spin.gplus.add(g)
        else:
            return
        return 'Added group %s' % string
    else:
        if type == '-':
            if g in spin.pplus.all():
                spin.gplus.remove(g)
            elif g not in spin.gminus.all():
                spin.gminus.add(g)
            else:
                return
            return 'Removed group %s' % string
        else:
            return

        return


def add_rem_packages(spin, type, string):
    """
    $function_name
    """
    if string:
        p = package(string)
    else:
        return
    if type == '+':
        if p in spin.pminus.all():
            spin.pminus.remove(p)
        elif p not in spin.pplus.all():
            spin.pplus.add(p)
        else:
            return
        return 'Added package %s' % string
    else:
        if type == '-':
            if p in spin.pplus.all():
                spin.pplus.remove(p)
            elif p not in spin.pminus.all():
                spin.pminus.add(p)
            else:
                return
            return 'Removed package %s' % string
        else:
            return

        return


def select_helper(spin_id, type, action, string):
    """
    helper to select/deselect package/groups
    """
    spin = get_spin(spin_id)
    if type == 'p':
        return add_rem_packages(spin, action, string)
    else:
        if type == 'g':
            return add_rem_groups(spin, action, string)
        else:
            return

        return


def handle_uploaded_ks(uploaded_ks):
    ks_path = os.path.join(settings.MEDIA_ROOT, uploaded_ks._name)
    print ks_path
    destination = open(ks_path, 'wb+')
    for chunk in uploaded_ks.chunks():
        destination.write(chunk)

    destination.close()