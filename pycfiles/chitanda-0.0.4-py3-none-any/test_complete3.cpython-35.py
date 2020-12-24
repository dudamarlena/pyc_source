# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/integration/complete/test_complete3.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 6743 bytes
from __future__ import print_function
from builtins import zip
from chisubmit.tests.common import cli_test, ChisubmitCLITestCase
from chisubmit.common.utils import get_datetime_now_utc, set_testing_now
from chisubmit.common import CHISUBMIT_SUCCESS, CHISUBMIT_FAIL
from datetime import timedelta
import time

class CLICompleteWorkflowCancelSubmission(ChisubmitCLITestCase):
    fixtures = [
     'admin_user']

    @cli_test
    def test_complete_with_submission_cancelling(self, runner):
        course_id = 'cmsc40300'
        course_name = 'Foobarmentals of Foobar II'
        admin_id = 'admin'
        instructor_ids = ['instructor']
        grader_ids = ['grader']
        student_ids = ['student1', 'student2', 'student3', 'student4']
        all_users = instructor_ids + grader_ids + student_ids
        admin, instructors, graders, students = self.create_clients(runner, admin_id, instructor_ids, grader_ids, student_ids, course_id, verbose=True)
        self.create_users(admin, all_users)
        self.create_course(admin, course_id, course_name)
        result = admin.run('admin course set-attribute %s default_extensions 3' % course_id)
        self.assertEqual(result.exit_code, 0)
        result = admin.run('admin course set-attribute %s extension_policy per-student' % course_id)
        self.assertEqual(result.exit_code, 0)
        self.add_users_to_course(admin, course_id, instructors, graders, students)
        deadline = get_datetime_now_utc() - timedelta(hours=23)
        deadline = deadline.isoformat(sep=' ')
        result = instructors[0].run('instructor assignment add', [
         'pa1', 'Programming Assignment 1', deadline])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor assignment set-attribute', [
         'pa1', 'max_students', '2'])
        self.assertEqual(result.exit_code, 0)
        teams = [
         'student1-student2',
         'student3-student4']
        students_team = [
         (
          students[0], students[1]),
         (
          students[2], students[3])]
        self.register_team(students_team[0], teams[0], 'pa1', course_id)
        self.register_team(students_team[1], teams[1], 'pa1', course_id)
        _, _, team_commits = self.create_team_repos(admin, course_id, teams[0:2], students_team[0:2])
        result = students_team[0][0].run('student assignment cancel-submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)
        result = students_team[0][0].run('student assignment submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        result = students_team[1][0].run('student assignment submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        result = students_team[0][0].run('student assignment cancel-submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        result = students_team[0][0].run('student assignment cancel-submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)
        result = students_team[1][0].run('student assignment submit', [
         'pa1', '--yes', '--commit-sha', team_commits[1][0].hexsha])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        new_now = get_datetime_now_utc() + timedelta(hours=2)
        set_testing_now(new_now)
        print()
        print("~~~ Time has moved 'forward' by two hours ~~~")
        print()
        result = students_team[1][0].run('student assignment cancel-submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        result = students_team[1][0].run('student assignment submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        new_now = get_datetime_now_utc() + timedelta(hours=24)
        set_testing_now(new_now)
        print()
        print("~~~ Time has moved 'forward' by 24 hours ~~~")
        print()
        result = instructors[0].run('instructor grading create-grading-repos', ['--master', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = students_team[0][0].run('student assignment submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        result = students_team[1][0].run('student assignment submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)
        result = students_team[1][0].run('student assignment cancel-submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)
        for team, student_team in zip(teams, students_team):
            result = student_team[0].run('student team show', [team])
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)