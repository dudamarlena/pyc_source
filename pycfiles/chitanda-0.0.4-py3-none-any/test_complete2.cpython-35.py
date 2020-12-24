# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/integration/complete/test_complete2.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 11558 bytes
from builtins import zip
from chisubmit.tests.common import cli_test, ChisubmitCLITestCase
from chisubmit.common.utils import get_datetime_now_utc
from chisubmit.common import CHISUBMIT_SUCCESS, CHISUBMIT_FAIL
from datetime import timedelta
from chisubmit.backend.api.models import Course, get_user_by_username

class CLICompleteWorkflowExtensionsPerStudent(ChisubmitCLITestCase):
    fixtures = [
     'admin_user']

    @cli_test
    def test_complete_with_extensions_per_student(self, runner):
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
        course = Course.get_by_course_id(course_id)
        self.assertIsNotNone(course)
        self.assertEqual(course.name, course_name)
        result = admin.run('admin course set-attribute %s default_extensions 3' % course_id)
        self.assertEqual(result.exit_code, 0)
        result = admin.run('admin course set-attribute %s extension_policy per-student' % course_id)
        self.assertEqual(result.exit_code, 0)
        self.add_users_to_course(admin, course_id, instructors, graders, students)
        deadline = get_datetime_now_utc() - timedelta(hours=23)
        deadline = deadline.replace(tzinfo=None).isoformat(sep=' ')
        result = instructors[0].run('instructor assignment add', [
         'pa1', 'Programming Assignment 1', deadline])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor assignment set-attribute', [
         'pa1', 'max_students', '2'])
        self.assertEqual(result.exit_code, 0)
        deadline = get_datetime_now_utc() - timedelta(hours=47)
        deadline = deadline.isoformat(sep=' ')
        result = instructors[0].run('instructor assignment add', [
         'pa2', 'Programming Assignment 2', deadline])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor assignment set-attribute', [
         'pa2', 'max_students', '2'])
        self.assertEqual(result.exit_code, 0)
        deadline = get_datetime_now_utc() - timedelta(hours=47)
        deadline = deadline.isoformat(sep=' ')
        result = instructors[0].run('instructor assignment add', [
         'pa3', 'Programming Assignment 3', deadline])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor assignment set-attribute', [
         'pa3', 'max_students', '2'])
        self.assertEqual(result.exit_code, 0)
        deadline = get_datetime_now_utc() - timedelta(hours=23)
        deadline = deadline.replace(tzinfo=None).isoformat(sep=' ')
        result = instructors[0].run('instructor assignment add', [
         'pa4', 'Programming Assignment 4', deadline])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor assignment set-attribute', [
         'pa4', 'max_students', '2'])
        self.assertEqual(result.exit_code, 0)
        deadline = get_datetime_now_utc() + timedelta(hours=2)
        deadline = deadline.replace(tzinfo=None).isoformat(sep=' ')
        result = instructors[0].run('instructor assignment add', [
         'pa5', 'Programming Assignment 5', deadline])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor assignment set-attribute', [
         'pa5', 'max_students', '2'])
        self.assertEqual(result.exit_code, 0)
        teams = [
         'student1-student2',
         'student3-student4',
         'student1-student3',
         'student2-student4']
        students_team = [
         (
          students[0], students[1]),
         (
          students[2], students[3]),
         (
          students[0], students[2]),
         (
          students[1], students[3])]
        self.register_team(students_team[0], teams[0], 'pa1', course_id)
        self.register_team(students_team[1], teams[1], 'pa2', course_id)
        team_git_paths, team_git_repos, team_commits = self.create_team_repos(admin, course_id, teams[0:2], students_team[0:2])
        self.register_team(students_team[2], teams[2], 'pa3', course_id)
        self.register_team(students_team[2], teams[2], 'pa4', course_id)
        self.register_team(students_team[2], teams[2], 'pa5', course_id)
        self.register_team(students_team[3], teams[3], 'pa3', course_id)
        self.register_team(students_team[3], teams[3], 'pa4', course_id)
        self.register_team(students_team[3], teams[3], 'pa5', course_id)
        x, y, z = self.create_team_repos(admin, course_id, teams[2:4], students_team[2:4])
        team_git_paths += x
        team_git_repos += y
        team_commits += z
        for s in students:
            result = s.run('student course show-extensions')
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        result = students_team[0][0].run('student assignment submit', [
         'pa1', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        s1 = course.get_student(get_user_by_username(students_team[0][0].user_id))
        s2 = course.get_student(get_user_by_username(students_team[0][1].user_id))
        t = course.get_team(teams[0])
        self.assertEqual(t.get_extensions_available(), 2)
        self.assertEqual(s1.get_extensions_available(), 2)
        self.assertEqual(s2.get_extensions_available(), 2)
        for s in students:
            result = s.run('student course show-extensions')
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        result = students_team[1][0].run('student assignment submit', [
         'pa2', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        s1 = course.get_student(get_user_by_username(students_team[1][0].user_id))
        s2 = course.get_student(get_user_by_username(students_team[1][1].user_id))
        t = course.get_team(teams[1])
        self.assertEqual(t.get_extensions_available(), 1)
        self.assertEqual(s1.get_extensions_available(), 1)
        self.assertEqual(s2.get_extensions_available(), 1)
        for s in students:
            result = s.run('student course show-extensions')
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        result = students_team[0][0].run('student team show', [teams[0]])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        result = students_team[1][0].run('student team show', [teams[1]])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        result = students_team[2][0].run('student assignment submit', [
         'pa3', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_FAIL)
        s1 = course.get_student(get_user_by_username(students_team[2][0].user_id))
        s2 = course.get_student(get_user_by_username(students_team[2][1].user_id))
        t = course.get_team(teams[2])
        self.assertEqual(t.get_extensions_available(), 1)
        self.assertEqual(s1.get_extensions_available(), 2)
        self.assertEqual(s2.get_extensions_available(), 1)
        result = students_team[2][0].run('student assignment submit', [
         'pa4', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        s1 = course.get_student(get_user_by_username(students_team[2][0].user_id))
        s2 = course.get_student(get_user_by_username(students_team[2][1].user_id))
        t = course.get_team(teams[2])
        self.assertEqual(t.get_extensions_available(), 0)
        self.assertEqual(s1.get_extensions_available(), 1)
        self.assertEqual(s2.get_extensions_available(), 0)
        for s in students:
            result = s.run('student course show-extensions')
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        result = students_team[2][0].run('student assignment submit', [
         'pa5', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        s1 = course.get_student(get_user_by_username(students_team[2][0].user_id))
        s2 = course.get_student(get_user_by_username(students_team[2][1].user_id))
        t = course.get_team(teams[2])
        self.assertEqual(t.get_extensions_available(), 0)
        self.assertEqual(s1.get_extensions_available(), 1)
        self.assertEqual(s2.get_extensions_available(), 0)
        for s in students:
            result = s.run('student course show-extensions')
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        result = students_team[3][0].run('student assignment submit', [
         'pa5', '--yes'])
        self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
        s1 = course.get_student(get_user_by_username(students_team[3][0].user_id))
        s2 = course.get_student(get_user_by_username(students_team[3][1].user_id))
        t = course.get_team(teams[3])
        self.assertEqual(t.get_extensions_available(), 1)
        self.assertEqual(s1.get_extensions_available(), 2)
        self.assertEqual(s2.get_extensions_available(), 1)
        for team, student_team in zip(teams, students_team):
            result = student_team[0].run('student team show', [team])
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)

        for s in students:
            result = s.run('student course show-extensions')
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)