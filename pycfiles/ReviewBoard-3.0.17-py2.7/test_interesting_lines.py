# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_interesting_lines.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.diffviewer.myersdiff import MyersDiffer
from reviewboard.testing import TestCase

class InterestingLinesTest(TestCase):
    """Unit tests for interesting lines scanner in differ."""

    def test_csharp(self):
        """Testing interesting lines scanner with a C# file"""
        a = b'public class HelloWorld {\n    public static void Main() {\n        System.Console.WriteLine("Hello world!");\n    }\n}\n'
        b = b'/*\n * The Hello World class.\n */\npublic class HelloWorld\n{\n    /*\n     * The main function in this class.\n     */\n    public static void Main()\n    {\n        /*\n         * Print "Hello world!" to the screen.\n         */\n        System.Console.WriteLine("Hello world!");\n    }\n}\n'
        lines = self._get_lines(a, b, b'helloworld.cs')
        self.assertEqual(len(lines[0]), 2)
        self.assertEqual(lines[0][0], (0, 'public class HelloWorld {\n'))
        self.assertEqual(lines[0][1], (1, '    public static void Main() {\n'))
        self.assertEqual(lines[1][0], (3, 'public class HelloWorld\n'))
        self.assertEqual(lines[1][1], (8, '    public static void Main()\n'))

    def test_java(self):
        """Testing interesting lines scanner with a Java file"""
        a = b'class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello world!");\n    }\n}\n'
        b = b'/*\n * The Hello World class.\n */\nclass HelloWorld\n{\n    /*\n     * The main function in this class.\n     */\n    public static void main(String[] args)\n    {\n        /*\n         * Print "Hello world!" to the screen.\n         */\n        System.out.println("Hello world!");\n    }\n}\n'
        lines = self._get_lines(a, b, b'helloworld.java')
        self.assertEqual(len(lines[0]), 2)
        self.assertEqual(lines[0][0], (0, 'class HelloWorld {\n'))
        self.assertEqual(lines[0][1], (1, '    public static void main(String[] args) {\n'))
        self.assertEqual(len(lines[1]), 2)
        self.assertEqual(lines[1][0], (3, 'class HelloWorld\n'))
        self.assertEqual(lines[1][1], (8, '    public static void main(String[] args)\n'))

    def test_javascript(self):
        """Testing interesting lines scanner with a JavaScript file"""
        a = b'function helloWorld() {\n    alert("Hello world!");\n}\n\nvar data = {\n    helloWorld2: function() {\n        alert("Hello world!");\n    }\n}\n\nvar helloWorld3 = function() {\n    alert("Hello world!");\n}\n'
        b = b'/*\n * Prints "Hello world!"\n */\nfunction helloWorld()\n{\n    alert("Hello world!");\n}\n\nvar data = {\n    /*\n     * Prints "Hello world!"\n     */\n    helloWorld2: function()\n    {\n        alert("Hello world!");\n    }\n}\n\nvar helloWorld3 = function()\n{\n    alert("Hello world!");\n}\n'
        lines = self._get_lines(a, b, b'helloworld.js')
        self.assertEqual(len(lines[0]), 3)
        self.assertEqual(lines[0][0], (0, 'function helloWorld() {\n'))
        self.assertEqual(lines[0][1], (5, '    helloWorld2: function() {\n'))
        self.assertEqual(lines[0][2], (10, 'var helloWorld3 = function() {\n'))
        self.assertEqual(len(lines[1]), 3)
        self.assertEqual(lines[1][0], (3, 'function helloWorld()\n'))
        self.assertEqual(lines[1][1], (12, '    helloWorld2: function()\n'))
        self.assertEqual(lines[1][2], (18, 'var helloWorld3 = function()\n'))

    def test_objective_c(self):
        """Testing interesting lines scanner with an Objective C file"""
        a = b'@interface MyClass : Object\n- (void) sayHello;\n@end\n\n@implementation MyClass\n- (void) sayHello {\n    printf("Hello world!");\n}\n@end\n'
        b = b'@interface MyClass : Object\n- (void) sayHello;\n@end\n\n@implementation MyClass\n/*\n * Prints Hello world!\n */\n- (void) sayHello\n{\n    printf("Hello world!");\n}\n@end\n'
        lines = self._get_lines(a, b, b'helloworld.m')
        self.assertEqual(len(lines[0]), 3)
        self.assertEqual(lines[0][0], (0, '@interface MyClass : Object\n'))
        self.assertEqual(lines[0][1], (4, '@implementation MyClass\n'))
        self.assertEqual(lines[0][2], (5, '- (void) sayHello {\n'))
        self.assertEqual(len(lines[1]), 3)
        self.assertEqual(lines[1][0], (0, '@interface MyClass : Object\n'))
        self.assertEqual(lines[1][1], (4, '@implementation MyClass\n'))
        self.assertEqual(lines[1][2], (8, '- (void) sayHello\n'))

    def test_perl(self):
        """Testing interesting lines scanner with a Perl file"""
        a = b'sub helloWorld {\n    print "Hello world!"\n}\n'
        b = b'# Prints Hello World\nsub helloWorld\n{\n    print "Hello world!"\n}\n'
        lines = self._get_lines(a, b, b'helloworld.pl')
        self.assertEqual(len(lines[0]), 1)
        self.assertEqual(lines[0][0], (0, 'sub helloWorld {\n'))
        self.assertEqual(len(lines[1]), 1)
        self.assertEqual(lines[1][0], (1, 'sub helloWorld\n'))

    def test_php(self):
        """Testing interesting lines scanner with a PHP file"""
        a = b'<?php\nclass HelloWorld {\n    function helloWorld() {\n        print "Hello world!";\n    }\n}\n?>\n'
        b = b'<?php\n/*\n * Hello World class\n */\nclass HelloWorld\n{\n    /*\n     * Prints Hello World\n     */\n    function helloWorld()\n    {\n        print "Hello world!";\n    }\n\n    public function foo() {\n        print "Hello world!";\n    }\n}\n?>\n'
        lines = self._get_lines(a, b, b'helloworld.php')
        self.assertEqual(len(lines[0]), 2)
        self.assertEqual(lines[0][0], (1, 'class HelloWorld {\n'))
        self.assertEqual(lines[0][1], (2, '    function helloWorld() {\n'))
        self.assertEqual(len(lines[1]), 3)
        self.assertEqual(lines[1][0], (4, 'class HelloWorld\n'))
        self.assertEqual(lines[1][1], (9, '    function helloWorld()\n'))
        self.assertEqual(lines[1][2], (14, '    public function foo() {\n'))

    def test_python(self):
        """Testing interesting lines scanner with a Python file"""
        a = b'class HelloWorld:\n    def main(self):\n        print "Hello World"\n'
        b = b'class HelloWorld:\n    """The Hello World class"""\n\n    def main(self):\n        """The main function in this class."""\n\n        # Prints "Hello world!" to the screen.\n        print "Hello world!"\n'
        lines = self._get_lines(a, b, b'helloworld.py')
        self.assertEqual(len(lines[0]), 2)
        self.assertEqual(lines[0][0], (0, 'class HelloWorld:\n'))
        self.assertEqual(lines[0][1], (1, '    def main(self):\n'))
        self.assertEqual(len(lines[1]), 2)
        self.assertEqual(lines[1][0], (0, 'class HelloWorld:\n'))
        self.assertEqual(lines[1][1], (3, '    def main(self):\n'))

    def test_ruby(self):
        """Testing interesting lines scanner with a Ruby file"""
        a = b'class HelloWorld\n    def helloWorld\n        puts "Hello world!"\n    end\nend\n'
        b = b'# Hello World class\nclass HelloWorld\n    # Prints Hello World\n    def helloWorld()\n        puts "Hello world!"\n    end\nend\n'
        lines = self._get_lines(a, b, b'helloworld.rb')
        self.assertEqual(len(lines[0]), 2)
        self.assertEqual(lines[0][0], (0, 'class HelloWorld\n'))
        self.assertEqual(lines[0][1], (1, '    def helloWorld\n'))
        self.assertEqual(len(lines[1]), 2)
        self.assertEqual(lines[1][0], (1, 'class HelloWorld\n'))
        self.assertEqual(lines[1][1], (3, '    def helloWorld()\n'))

    def _get_lines(self, a, b, filename):
        differ = MyersDiffer(a.splitlines(True), b.splitlines(True))
        differ.add_interesting_lines_for_headers(filename)
        list(differ.get_opcodes())
        return (
         differ.get_interesting_lines(b'header', False),
         differ.get_interesting_lines(b'header', True))