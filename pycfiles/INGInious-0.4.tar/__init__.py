# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dervalguillaume/PycharmProjects/INGInious/inginious/frontend/webapp/plugins/scoreboard/__init__.py
# Compiled at: 2016-02-11 04:12:59
""" A scoreboard, based on the usage of the "custom" dict in submissions.
    It uses the key "score" to retrieve score from submissions
"""
from collections import OrderedDict
import web
from inginious.frontend.webapp.pages.utils import INGIniousPage

class ScoreBoardCourse(INGIniousPage):

    def GET(self, courseid):
        """ GET request """
        course = self.course_factory.get_course(courseid)
        scoreboards = course.get_descriptor().get('scoreboard', [])
        try:
            names = {i:val['name'] for i, val in enumerate(scoreboards)}
        except:
            raise web.notfound('Invalid configuration')

        if len(names) == 0:
            raise web.notfound()
        return self.template_helper.get_custom_template_renderer('frontend/webapp/plugins/scoreboard', '../../templates/layout').main(course, names)


def sort_func(overall_result_per_user, reversed):

    def sf(user):
        score = overall_result_per_user[user]['total']
        solved = overall_result_per_user[user]['solved']
        return (
         -solved, -(reversed or score) if 1 else score)

    return sf


class ScoreBoard(INGIniousPage):

    def GET(self, courseid, scoreboardid):
        """ GET request """
        course = self.course_factory.get_course(courseid)
        scoreboards = course.get_descriptor().get('scoreboard', [])
        try:
            scoreboardid = int(scoreboardid)
            scoreboard_name = scoreboards[scoreboardid]['name']
            scoreboard_content = scoreboards[scoreboardid]['content']
            scoreboard_reverse = bool(scoreboards[scoreboardid].get('reverse', False))
        except:
            raise web.notfound()

        if isinstance(scoreboard_content, basestring):
            scoreboard_content = OrderedDict((scoreboard_content, 1))
        if isinstance(scoreboard_content, list):
            scoreboard_content = OrderedDict([ (entry, 1) for entry in scoreboard_content ])
        if not isinstance(scoreboard_content, OrderedDict):
            scoreboard_content = OrderedDict(scoreboard_content.iteritems())
        task_names = {}
        for taskid in scoreboard_content:
            try:
                task_names[taskid] = course.get_task(taskid).get_name()
            except:
                raise web.notfound('Unknown task id ' + taskid)

        results = self.database.submissions.find({'courseid': courseid, 
           'taskid': {'$in': scoreboard_content.keys()}, 'custom.score': {'$exists': True}, 'result': 'success'}, [
         'taskid', 'username', 'custom.score'])
        result_per_user = {}
        users = set()
        for submission in results:
            if not isinstance(submission['username'], list):
                submission['username'] = [
                 submission['username']]
            submission['username'] = tuple(submission['username'])
            if submission['username'] not in result_per_user:
                result_per_user[submission['username']] = {}
            if submission['taskid'] not in result_per_user[submission['username']]:
                result_per_user[submission['username']][submission['taskid']] = submission['custom']['score']
            else:
                current_score = result_per_user[submission['username']][submission['taskid']]
                new_score = submission['custom']['score']
                task_reversed = scoreboard_reverse != (scoreboard_content[submission['taskid']] < 0)
                if task_reversed and current_score > new_score:
                    result_per_user[submission['username']][submission['taskid']] = new_score
                elif not task_reversed and current_score < new_score:
                    result_per_user[submission['username']][submission['taskid']] = new_score
                for user in submission['username']:
                    users.add(user)

        users_realname = {}
        for username, userinfo in self.user_manager.get_users_info(users).iteritems():
            users_realname[username] = userinfo[0] if userinfo else username

        overall_result_per_user = {}
        for key, val in result_per_user.iteritems():
            total = 0
            solved = 0
            for taskid, coef in scoreboard_content.iteritems():
                if taskid in val:
                    total += val[taskid] * coef
                    solved += 1

            overall_result_per_user[key] = {'total': total, 'solved': solved}

        sorted_users = list(overall_result_per_user.keys())
        sorted_users = sorted(sorted_users, key=sort_func(overall_result_per_user, scoreboard_reverse))
        table = []
        if len(scoreboard_content) == 1:
            header = [
             '', 'Student(s)', 'Score']
            emphasized_columns = [2]
        else:
            header = [
             '', 'Student(s)', 'Solved', 'Total score'] + [ task_names[taskid] for taskid in scoreboard_content.keys() ]
            emphasized_columns = [2, 3]
        old_score = ()
        rank = 0
        for user in sorted_users:
            line = []
            if old_score != (overall_result_per_user[user]['solved'], overall_result_per_user[user]['total']):
                rank += 1
                old_score = (overall_result_per_user[user]['solved'], overall_result_per_user[user]['total'])
                line.append(rank)
            else:
                line.append('')
            line.append((',').join(sorted([ users_realname[u] for u in user ])))
            if len(scoreboard_content) == 1:
                line.append(overall_result_per_user[user]['total'])
            else:
                line.append(overall_result_per_user[user]['solved'])
                line.append(overall_result_per_user[user]['total'])
                for taskid in scoreboard_content:
                    line.append(result_per_user[user].get(taskid, ''))

            table.append(line)

        renderer = self.template_helper.get_custom_template_renderer('frontend/webapp/plugins/scoreboard', '../../templates/layout')
        return renderer.scoreboard(course, scoreboardid, scoreboard_name, header, table, emphasized_columns)


def course_menu(course, template_helper):
    """ Displays the link to the scoreboards on the course page, if the plugin is activated for this course """
    scoreboards = course.get_descriptor().get('scoreboard', [])
    if scoreboards != []:
        return str(template_helper.get_custom_template_renderer('frontend/webapp/plugins/scoreboard').course_menu(course))
    else:
        return
        return


def task_menu(course, task, template_helper):
    """ Displays the link to the scoreboards on the task page, if the plugin is activated for this course and the task is used in scoreboards """
    scoreboards = course.get_descriptor().get('scoreboard', [])
    try:
        tolink = []
        for sid, scoreboard in enumerate(scoreboards):
            if task.get_id() in scoreboard['content']:
                tolink.append((sid, scoreboard['name']))

        if tolink:
            return str(template_helper.get_custom_template_renderer('frontend/webapp/plugins/scoreboard').task_menu(course, tolink))
        return
    except:
        return

    return


def init(plugin_manager, _, _2, _3):
    """
        Init the plugin.
        Available configuration in configuration.yaml:
        ::

            - plugin_module: "webapp.plugins.scoreboard"

        Available configuration in course.yaml:
        ::

            - scoreboard: #you can define multiple scoreboards
                - content: "taskid1" #creates a scoreboard for taskid1
                  name: "Scoreboard task 1"
                - content: ["taskid2", "taskid3"] #creates a scoreboard for taskid2 and taskid3 (sum of both score is taken as overall score)
                  name: "Scoreboard for task 2 and 3"
                - content: {"taskid4": 2, "taskid5": 3} #creates a scoreboard where overall score is 2*score of taskid4 + 3*score of taskid5
                  name: "Another scoreboard"
                  reverse: True #reverse the score (less is better)
    """
    page_pattern_course = '/scoreboard/(.+)'
    page_pattern_scoreboard = '/scoreboard/(.+)/(.+)'
    plugin_manager.add_page(page_pattern_course, ScoreBoardCourse)
    plugin_manager.add_page(page_pattern_scoreboard, ScoreBoard)
    plugin_manager.add_hook('course_menu', course_menu)
    plugin_manager.add_hook('task_menu', task_menu)