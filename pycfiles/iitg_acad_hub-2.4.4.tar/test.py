# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/Desktop/iitg_acad_hub/tests/test.py
# Compiled at: 2016-04-25 07:51:06
"""@package docstring
Documentation for this module.

Testing Module
"""
import unittest
from iitg_acad_hub.details import semFinder, depFinder
from iitg_acad_hub.notes import *
from iitg_acad_hub.webcrawler import getCourseBooks, showBooks
import json, os

class unitTester(unittest.TestCase):

    def test_is_correct_sem(self):
        """Test function to test the semester returned on giving a roll number to the function semFinder
                """
        rolls = [
         '120101039', '130101058', '140101052', '150101043']
        sems = [8, 6, 4, 2]
        for i in range(len(rolls)):
            self.assertEqual(semFinder(rolls[i]), sems[i])

    def test_is_correct_dep(self):
        """Test function to test the department returned on giving a roll number to the function depFinder
                """
        Rollnumber = [
         '140101057', '140102032', '140103078', '140104080', '140105082', '140106035', '140407025', '140508075', '140021150', '141022402', '140123024']
        Department = ['CSE', 'ECE', 'ME', 'CE', 'bdes', 'BT', 'CL', 'EEE', 'EPh', 'CST', 'MC']
        for i in range(len(Rollnumber)):
            self.assertEqual(depFinder(Rollnumber[i]), Department[i])

    def test_is_uploading(self):
        """Test function to test the uploading of notes
                """
        with open('utest.txt', 'w') as (f):
            f.write('Test')
        self.assertEqual(uploadFile('utest.txt', '100101001', 'TEST'), 200)
        os.remove('utest.txt')

    def test_is_listing(self):
        """Test function to test if the list of uploaded notes for a course is appropriately returned
                """
        self.assertEqual(listUploads('TEST')[1][0], 'test.txt')

    def test_is_downloading(self):
        """Test function to test the downloading of notes
                """
        downloadFile('test.txt', os.getcwd(), 'TEST', '100101001', '0.00(0)')
        x = ''
        with open('test.txt', 'r') as (f):
            x = f.readline()
        self.assertEqual(x, 'DownloadTest\n')
        os.remove('test.txt')

    def test_courses(self):
        """Test function to test if the correct course information is returned for all the available semesters and departments.
                It checks the returned output with the data dumped in "course.json" file
                """
        depts = [
         'CSE', 'ECE', 'ME', 'CE', 'bdes', 'BT', 'CL', 'EEE', 'EPh', 'CST', 'MC']
        with open('tests/course.json', 'r') as (f):
            data = json.load(f)
        j = 0
        for dept in depts:
            for i in range(1, 9):
                self.assertEqual(showBooks(dept, i, 'courses'), data[j])
                j += 1

    def test_course_books(self):
        """Test function to test if the correct books information is returned for all the available semesters and departments.
                It checks the returned output with the data dumped in "books.json" file
                """
        depts = [
         'CSE', 'ECE', 'ME', 'CE', 'bdes', 'BT', 'CL', 'EEE', 'EPh', 'CST', 'MC']
        with open('tests/books.json', 'r') as (f):
            data = json.load(f)
        j = 0
        for dept in depts:
            for i in range(1, 9):
                x = showBooks(dept, i, 'books')
                y = []
                for i in x:
                    y.append(list(i))

                self.assertEqual(y, data[j])
                j += 1


if __name__ == '__main__':
    unittest.main()