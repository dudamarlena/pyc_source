# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/tests/integration/complete/test_complete6.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 14841 bytes
from __future__ import print_function
from builtins import zip
from chisubmit.tests.common import cli_test, ChisubmitCLITestCase
from chisubmit.common.utils import get_datetime_now_utc, convert_datetime_to_local, set_testing_now
from chisubmit.common import CHISUBMIT_SUCCESS, CHISUBMIT_FAIL
from datetime import timedelta
import os

class CLICompleteWorkflowMultipleInstructorsMultipleGraders(ChisubmitCLITestCase):
    fixtures = [
     'admin_user']

    @cli_test
    def test_complete_with_multiple_instructors_multiple_graders(self, runner):
        course_id = 'cmsc40200'
        course_name = 'Foobarmentals of Foobar'
        admin_id = 'admin'
        instructor_ids = ['instructor1', 'instructor2']
        grader_ids = ['grader1', 'grader2']
        student_ids = ['student1', 'student2', 'student3', 'student4']
        all_users = instructor_ids + grader_ids + student_ids
        admin, instructors, graders, students = self.create_clients(runner, admin_id, instructor_ids, grader_ids, student_ids, course_id, verbose=True)
        self.create_users(admin, all_users)
        self.create_course(admin, course_id, course_name)
        self.add_users_to_course(admin, course_id, instructors, graders, students)
        students_team = [[s] for s in students]
        deadline = get_datetime_now_utc() + timedelta(hours=1)
        deadline = convert_datetime_to_local(deadline)
        deadline = deadline.replace(tzinfo=None).isoformat(sep=' ')
        result = instructors[0].run('instructor assignment add', [
         'pa1', 'Programming Assignment 1', deadline])
        self.assertEqual(result.exit_code, 0)
        pa1_rubric = 'Points:\n    - The PA1 Tests:\n        Points Possible: 50\n        Points Obtained: \n\n    - The PA1 Design:\n        Points Possible: 50\n        Points Obtained: \n        \nTotal Points: 0 / 100\n'
        with open('pa1.rubric.txt', 'w') as (f):
            f.write(pa1_rubric)
        result = instructors[0].run('instructor assignment add-rubric', [
         'pa1', 'pa1.rubric.txt'])
        self.assertEqual(result.exit_code, 0)
        result = admin.run('admin course show', ['--include-users', '--include-assignments', course_id])
        self.assertEqual(result.exit_code, 0)
        for student_id, student in zip(student_ids, students):
            self.register_team([student], student_id, 'pa1', course_id)

        for student_id, student in zip(student_ids, students):
            result = student.run('student team list')
            self.assertEqual(result.exit_code, 0)
            self.assertIn(student_id, result.output)
            result = student.run('student team show', [student_id])
            self.assertEqual(result.exit_code, 0)

        result = instructors[0].run('instructor team list')
        self.assertEqual(result.exit_code, 0)
        for student_id in student_ids:
            result = instructors[0].run('instructor team show', [student_id])
            self.assertEqual(result.exit_code, 0)

        student_git_paths, student_git_repos, team_commits = self.create_team_repos(admin, course_id, student_ids, students_team)
        for student_id, student in zip(student_ids, students):
            result = student.run('student assignment submit', [
             'pa1', '--yes'])
            self.assertEqual(result.exit_code, CHISUBMIT_SUCCESS)
            result = student.run('student team show', [student_id])
            self.assertEqual(result.exit_code, 0)

        new_now = get_datetime_now_utc() + timedelta(hours=2)
        set_testing_now(new_now)
        print()
        print("~~~ Time has moved 'forward' by two hours ~~~")
        print()
        result = instructors[0].run('instructor grading list-submissions', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading create-grading-repos', ['--master', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading assign-grader', ['pa1', 'student1', 'grader1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading assign-grader', ['pa1', 'student2', 'grader1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading assign-grader', ['pa1', 'student3', 'grader2'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading assign-grader', ['pa1', 'student4', 'grader2'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading list-grader-assignments', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading push-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading create-grading-repos', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = graders[0].run('grader pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        student1_grading_repo_path = 'chisubmit-test/repositories/%s/%s/%s' % (course_id, 'pa1', 'student1')
        student2_grading_repo_path = 'chisubmit-test/repositories/%s/%s/%s' % (course_id, 'pa1', 'student2')
        student_git_repos[0], student_git_paths[0] = graders[0].get_local_git_repository(student1_grading_repo_path)
        student_git_repos[1], student_git_paths[1] = graders[0].get_local_git_repository(student2_grading_repo_path)
        student1_rubric_path = '%s/pa1.rubric.txt' % student_git_paths[0]
        student2_rubric_path = '%s/pa1.rubric.txt' % student_git_paths[1]
        student1_rubric = 'Points:\n    - The PA1 Tests:\n        Points Possible: 50\n        Points Obtained: 45\n\n    - The PA1 Design:\n        Points Possible: 50\n        Points Obtained: 30\n        \nPenalties:\n    Used O(n^156) algorithm: -10\n    Submitted code in a Word document: -30\n\nBonuses:\n    Worked alone: 15\n\nTotal Points: 50 / 100\n\nComments: >\n    None'
        with open(student1_rubric_path, 'w') as (f):
            f.write(student1_rubric)
        result = graders[0].run('grader validate-rubrics', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        student_git_repos[0].index.add(['pa1.rubric.txt'])
        student_git_repos[0].index.commit('Finished grading')
        result = graders[0].run('grader push-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        student2_rubric = 'Points:\n    - The PA1 Tests:\n        Points Possible: 50\n        Points Obtained: 50\n\n    - The PA1 Design:\n        Points Possible: 50\n        Points Obtained: 45\n\nTotal Points: 95 / 100\n\nComments: >\n    Great job!'
        with open(student2_rubric_path, 'w') as (f):
            f.write(student2_rubric)
        result = graders[0].run('grader validate-rubrics', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        student_git_repos[1].index.add(['pa1.rubric.txt'])
        student_git_repos[1].index.commit('Finished grading')
        result = graders[0].run('grader push-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = graders[1].run('grader pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        student3_grading_repo_path = 'chisubmit-test/repositories/%s/%s/%s' % (course_id, 'pa1', 'student3')
        student4_grading_repo_path = 'chisubmit-test/repositories/%s/%s/%s' % (course_id, 'pa1', 'student4')
        student_git_repos[2], student_git_paths[2] = graders[1].get_local_git_repository(student3_grading_repo_path)
        student_git_repos[3], student_git_paths[3] = graders[1].get_local_git_repository(student4_grading_repo_path)
        student3_rubric_path = '%s/pa1.rubric.txt' % student_git_paths[2]
        student4_rubric_path = '%s/pa1.rubric.txt' % student_git_paths[3]
        result = graders[1].run('grader validate-rubrics', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        student_git_repos[2].index.add(['pa1.rubric.txt'])
        student_git_repos[2].index.commit('Added rubric')
        student_git_repos[3].index.add(['pa1.rubric.txt'])
        student_git_repos[3].index.commit('Added rubric')
        result = graders[1].run('grader push-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        student3_rubric = 'Points:\n    - The PA1 Tests:\n        Points Possible: 50\n        Points Obtained: 20\n\n    - The PA1 Design:\n        Points Possible: 50\n        Points Obtained: 15\n\nTotal Points: 35 / 100\n\nComments: >\n    Needs improvement!'
        with open(student3_rubric_path, 'w') as (f):
            f.write(student3_rubric)
        student4_rubric = 'Points:\n    - The PA1 Tests:\n        Points Possible: 50\n        Points Obtained: 35\n\n    - The PA1 Design:\n        Points Possible: 50\n        Points Obtained: \n\nTotal Points: 35 / 100\n\nComments: >\n'
        with open(student4_rubric_path, 'w') as (f):
            f.write(student4_rubric)
        result = graders[1].run('grader validate-rubrics', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        student_git_repos[2].index.add(['pa1.rubric.txt'])
        student_git_repos[2].index.commit('Finished grading')
        student_git_repos[3].index.add(['pa1.rubric.txt'])
        student_git_repos[3].index.commit('Grading in progress')
        result = graders[1].run('grader push-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        student4_rubric = 'Points:\n    - The PA1 Tests:\n        Points Possible: 50\n        Points Obtained: 35\n\n    - The PA1 Design:\n        Points Possible: 50\n        Points Obtained: 25\n\nTotal Points: 60 / 100\n\nComments: >\n'
        with open(student4_rubric_path, 'w') as (f):
            f.write(student4_rubric)
        result = graders[1].run('grader validate-rubrics', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        student_git_repos[3].index.add(['pa1.rubric.txt'])
        student_git_repos[3].index.commit('Finished grading')
        result = graders[1].run('grader push-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[1].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading pull-grading', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading show-grading-status', ['--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading collect-rubrics', ['pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading show-grading-status', ['--use-stored-grades', '--by-grader', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading list-grades')
        self.assertEqual(result.exit_code, 0)
        result = instructors[0].run('instructor grading push-grading', ['--to-students', '--yes', 'pa1'])
        self.assertEqual(result.exit_code, 0)
        for student_id, student in zip(student_ids, students):
            repo, path = student.get_local_git_repository(student_id)
            repo.remote('origin').pull('pa1-grading:pa1-grading')
            repo.heads['pa1-grading'].checkout()
            self.assertTrue(os.path.exists(path + '/pa1.rubric.txt'))