# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/app/controller/api.py
# Compiled at: 2016-08-05 05:22:40
import time, os
from utils import common, config
from flask import request, jsonify
import subprocess
from app import web
from app import CobraTaskInfo
from app import CobraProjects
from app import db
from pickup import GitTools, subversion
API_URL = '/api'

@web.route(API_URL + '/add', methods=['POST'])
def add_task():
    """ Add a new task api.
    post json to http://url/api/add_new_task
    example:
        {
            "key": "34b9a295d037d47eec3952e9dcdb6b2b",              // must, client key
            "target": "https://gitlab.com/username/project.git",    // must, gitlab address
            "branch": "master",                                     // must, the project branch
            "old_version": "old version here",                      // optional, if you choice diff scan mode, you should provide old version hash.
            "new_version": "new version here",                      // optional, if you choice diff scan mode, you should provide new version hash.
        }
    :return:
        The return value also in json format, usually is:
        {"code": 1001, "msg": "error reason or success."}
        code: 1005: Unknown Protocol
        code: 1004: Unknown error, if you see this error code, most time is cobra's database error.
        code: 1003: You support the parameters is not json.
        code: 1002: Some parameters is empty. More information in "msg".
        code: 1001: Success, no error.
    """
    result = {}
    data = request.json
    if not data or data == '':
        return jsonify(code=1003, msg='Only support json, please post json data.')
    else:
        key = data.get('key')
        if common.verify_key(key) is False:
            return jsonify(code=4002, msg='Key verify failed')
        target = data.get('target')
        branch = data.get('branch')
        new_version = data.get('new_version')
        old_version = data.get('old_version')
        if not key or key == '':
            return jsonify(code=1002, msg='key can not be empty.')
        if not target or target == '':
            return jsonify(code=1002, msg='url can not be empty.')
        if not branch or branch == '':
            return jsonify(code=1002, msg='branch can not be empty.')
        current_time = time.strftime('%Y-%m-%d %X', time.localtime())
        if '.git' in target:
            if 'gitlab' in target:
                username = config.Config('git', 'username').value
                password = config.Config('git', 'password').value
            else:
                username = False
                password = False
            gg = GitTools.Git(target, branch=branch, username=username, password=password)
            repo_author = gg.repo_author
            repo_name = gg.repo_name
            repo_directory = gg.repo_directory
            if gg.clone() is False:
                return jsonify(code=4001)
        else:
            if 'svn' in target:
                repo_name = 'mogujie'
                repo_author = 'all'
                repo_directory = os.path.join(config.Config('cobra', 'upload_directory').value, 'uploads/mogujie/')
            else:
                return jsonify(code=1005)
            if new_version == '' or old_version == '':
                scan_way = 1
            else:
                scan_way = 2
            task = CobraTaskInfo(target, branch, scan_way, new_version, old_version, None, None, None, 1, None, 0, current_time, current_time)
            p = CobraProjects.query.filter_by(repository=target).first()
            project = None
            if not p:
                project = CobraProjects(target, repo_name, repo_author, None, None, current_time, current_time)
                project_id = project.id
            else:
                project_id = p.id
            try:
                db.session.add(task)
                if not p:
                    db.session.add(project)
                db.session.commit()
                cobra_path = os.path.join(config.Config().project_directory, 'cobra.py')
                if os.path.isfile(cobra_path) is not True:
                    return jsonify(code=1004, msg='Cobra Not Found')
                subprocess.Popen([
                 'python', cobra_path, 'scan', '-p', str(project_id), '-i', str(task.id), '-t', repo_directory])
                subprocess.Popen([
                 'python', cobra_path, 'statistic', '-i', str(task.id), '-t', repo_directory])
                result['scan_id'] = task.id
                result['project_id'] = project_id
                result['msg'] = 'success'
                return jsonify(code=1001, result=result)
            except Exception as e:
                return jsonify(code=1004, msg='Unknown error, try again later?' + e.message)

        return


@web.route(API_URL + '/status', methods=['POST'])
def status_task():
    scan_id = request.json.get('scan_id')
    key = request.json.get('key')
    if common.verify_key(key) is False:
        return jsonify(code=4002, msg='Key verify failed')
    c = CobraTaskInfo.query.filter_by(id=scan_id).first()
    if not c:
        return jsonify(status=4004)
    status = {0: 'init', 1: 'scanning', 
       2: 'done', 
       3: 'error'}
    status_text = status[c.status]
    domain = config.Config('cobra', 'domain').value
    result = {'status': status_text, 
       'text': 'Success', 
       'report': 'http://' + domain + '/report/' + str(scan_id), 
       'allow_deploy': True}
    return jsonify(status=1001, result=result)