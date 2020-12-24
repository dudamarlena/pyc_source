# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/core/utils_db.py
# Compiled at: 2015-11-21 14:46:11
import os, json

def handle_db_after_an_install(pkg_type, pkg_to_install_name, branch_to_install, lang_cmd_for_install, db_pname):
    branch_to_install_dict = {'installation_lang_cmd': lang_cmd_for_install}
    if not os.path.exists(db_pname):
        with open(db_pname, 'w') as (f):
            db = {pkg_type: {pkg_to_install_name: {branch_to_install: branch_to_install_dict}}}
            json.dump(db, f, indent=4)
    elif os.path.exists(db_pname):
        with open(db_pname, 'r') as (f):
            db = json.load(f)
            if pkg_type in db:
                if pkg_to_install_name in db[pkg_type]:
                    if branch_to_install in db[pkg_type][pkg_to_install_name]:
                        pass
                    else:
                        db[pkg_type][pkg_to_install_name].update({branch_to_install: branch_to_install_dict})
                else:
                    db[pkg_type].update({pkg_to_install_name: {branch_to_install: branch_to_install_dict}})
            else:
                db.update({pkg_type: {pkg_to_install_name: {branch_to_install: branch_to_install_dict}}})
        with open(db_pname, 'w') as (f):
            json.dump(db, f, sort_keys=True, indent=4)


def get_lang_cmd_branch_was_installed_with(pkg_type, pkg_name, branch, db_pname):
    with open(db_pname, 'r') as (f):
        db = json.load(f)
        lang_branch_installed_with = db[pkg_type][pkg_name][branch]['installation_lang_cmd']
        return lang_branch_installed_with


def handle_db_for_removal(pkg_type, pkg_to_remove_name, branch_to_remove, db_pname):
    if os.path.exists(db_pname):
        with open(db_pname, 'r') as (f):
            db = json.load(f)
            if pkg_type in db:
                if pkg_to_remove_name in db[pkg_type]:
                    if branch_to_remove in db[pkg_type][pkg_to_remove_name]:
                        del db[pkg_type][pkg_to_remove_name][branch_to_remove]
        for pkg_type, pkgs_to_remove_dict in db.items():
            if not pkgs_to_remove_dict:
                del db[pkg_type]
            for pkg_to_remove, branches_to_remove_dict in pkgs_to_remove_dict.items():
                if not branches_to_remove_dict:
                    del db[pkg_type][pkg_to_remove]

        with open(db_pname, 'w') as (f):
            json.dump(db, f, sort_keys=True, indent=4)


def handle_db_for_branch_renaming(pkg_type, pkg_name, branch_orig_name, branch_renamed, db_pname):
    if os.path.exists(db_pname):
        with open(db_pname, 'r') as (f):
            db = json.load(f)
            if pkg_type in db:
                if pkg_name in db[pkg_type]:
                    if branch_orig_name in db[pkg_type][pkg_name]:
                        db[pkg_type][pkg_name][branch_renamed] = db[pkg_type][pkg_name].pop(branch_orig_name)
        with open(db_pname, 'w') as (f):
            json.dump(db, f, sort_keys=True, indent=4)