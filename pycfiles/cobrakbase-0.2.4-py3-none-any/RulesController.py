# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/app/controller/backend/RulesController.py
# Compiled at: 2016-08-01 04:00:02
import time
from flask import redirect, render_template, request, jsonify
from . import ADMIN_URL
from app import web, db
from app.models import CobraRules, CobraVuls, CobraLanguages
from app.CommonClass.ValidateClass import ValidateClass
__author__ = 'lightless'
__email__ = 'root@lightless.me'

@web.route(ADMIN_URL + '/rules/<int:page>', methods=['GET'])
def rules(page):
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    per_page = 10
    cobra_rules = CobraRules.query.order_by('id desc').limit(per_page).offset((page - 1) * per_page).all()
    cobra_vuls = CobraVuls.query.all()
    cobra_lang = CobraLanguages.query.all()
    all_vuls = {}
    all_language = {}
    all_level = {1: 'Low', 2: 'Medium', 3: 'High'}
    for vul in cobra_vuls:
        all_vuls[vul.id] = vul.name

    for lang in cobra_lang:
        all_language[lang.id] = lang.language

    status_desc = {1: 'ON', 0: 'OFF'}
    for rule in cobra_rules:
        try:
            rule.vul_id = all_vuls[rule.vul_id]
        except KeyError:
            rule.vul_id = 'Unknown Type'

        try:
            rule.status = status_desc[rule.status]
        except KeyError:
            rule.status = 'Unknown'

        try:
            rule.language = all_language[rule.language]
        except KeyError:
            rule.language = 'Unknown Language'

        try:
            rule.level = all_level[rule.level]
        except KeyError:
            rule.level = 'Unknown Level'

    data = {'rules': cobra_rules}
    return render_template('backend/rule/rules.html', data=data)


@web.route(ADMIN_URL + '/add_new_rule', methods=['GET', 'POST'])
def add_new_rule():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    if request.method == 'POST':
        vc = ValidateClass(request, 'vul_type', 'language', 'regex', 'regex_confirm', 'description', 'repair', 'level')
        ret, msg = vc.check_args()
        if not ret:
            return jsonify(tag='danger', msg=msg)
        current_time = time.strftime('%Y-%m-%d %X', time.localtime())
        rule = CobraRules(vc.vars.vul_type, vc.vars.language, vc.vars.regex, vc.vars.regex_confirm, vc.vars.description, vc.vars.repair, 1, vc.vars.level, current_time, current_time)
        try:
            db.session.add(rule)
            db.session.commit()
            return jsonify(tag='success', msg='add success.')
        except:
            return jsonify(tag='danger', msg='add failed, try again later?')

    else:
        vul_type = CobraVuls.query.all()
        languages = CobraLanguages.query.all()
        data = {'vul_type': vul_type, 
           'languages': languages}
        return render_template('backend/rule/add_new_rule.html', data=data)


@web.route(ADMIN_URL + '/del_rule', methods=['POST'])
def del_rule():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    vc = ValidateClass(request, 'rule_id')
    vc.check_args()
    vul_id = vc.vars.rule_id
    if vul_id:
        r = CobraRules.query.filter_by(id=vul_id).first()
        try:
            db.session.delete(r)
            db.session.commit()
            return jsonify(tag='success', msg='delete success.')
        except:
            return jsonify(tag='danger', msg='delete failed. Try again later?')

    else:
        return jsonify(tag='danger', msg='wrong id')


@web.route(ADMIN_URL + '/edit_rule/<int:rule_id>', methods=['GET', 'POST'])
def edit_rule(rule_id):
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    if request.method == 'POST':
        vc = ValidateClass(request, 'vul_type', 'language', 'regex', 'regex_confirm', 'description', 'rule_id', 'repair', 'status', 'level')
        ret, msg = vc.check_args()
        if not ret:
            return jsonify(tag='danger', msg=msg)
        r = CobraRules.query.filter_by(id=rule_id).first()
        r.vul_id = vc.vars.vul_type
        r.language = vc.vars.language
        r.regex = vc.vars.regex
        r.regex_confirm = vc.vars.regex_confirm
        r.description = vc.vars.description
        r.repair = vc.vars.repair
        r.status = vc.vars.status
        r.level = vc.vars.level
        r.updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
        try:
            db.session.add(r)
            db.session.commit()
            return jsonify(tag='success', msg='save success.')
        except:
            return jsonify(tag='danger', msg='save failed. Try again later?')

    else:
        r = CobraRules.query.filter_by(id=rule_id).first()
        vul_type = CobraVuls.query.all()
        languages = CobraLanguages.query.all()
        return render_template('backend/rule/edit_rule.html', data={'rule': r, 
           'all_vuls': vul_type, 
           'all_lang': languages})