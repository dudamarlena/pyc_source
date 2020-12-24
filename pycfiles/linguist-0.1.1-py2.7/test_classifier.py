# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_classifier.py
# Compiled at: 2013-04-25 10:01:56
from framework import LinguistTestBase, main
from libs.classifier import Classifier
from libs.tokenizer import Tokenizer
from libs.samples import DATA
TEST_FILE = '../samples/%s'

class TestClassifier(LinguistTestBase):

    def fixture(self, name):
        return open(TEST_FILE % name).read()

    def test_classify(self):
        db = {}
        Classifier.train(db, 'Ruby', self.fixture('Ruby/foo.rb'))
        Classifier.train(db, 'Objective-C', self.fixture('Objective-C/Foo.h'))
        Classifier.train(db, 'Objective-C', self.fixture('Objective-C/Foo.m'))
        rs = Classifier.classify(db, self.fixture('Objective-C/hello.m'))
        assert 'Objective-C' == rs[0][0]
        tokens = Tokenizer.tokenize(self.fixture('Objective-C/hello.m'))
        rs = Classifier.classify(db, tokens)
        assert 'Objective-C' == rs[0][0]

    def test_restricted_classify(self):
        db = {}
        Classifier.train(db, 'Ruby', self.fixture('Ruby/foo.rb'))
        Classifier.train(db, 'Objective-C', self.fixture('Objective-C/Foo.h'))
        Classifier.train(db, 'Objective-C', self.fixture('Objective-C/Foo.m'))
        rs = Classifier.classify(db, self.fixture('Objective-C/hello.m'), ['Objective-C'])
        assert 'Objective-C' == rs[0][0]
        rs = Classifier.classify(db, self.fixture('Objective-C/hello.m'), ['Ruby'])
        assert 'Ruby' == rs[0][0]

    def test_instance_classify_empty(self):
        rs = Classifier.classify(DATA, '')
        r = rs[0]
        assert r[1] < 0.5, str(r)

    def test_instance_classify_none(self):
        assert [] == Classifier.classify(DATA, None)
        return

    def test_classify_ambiguous_languages(self):
        """
        Samples.each do |sample|
          language  = Linguist::Language.find_by_name(sample[:language])
          languages = Language.find_by_filename(sample[:path]).map(&:name)
          next unless languages.length > 1

          results = Classifier.classify(Samples::DATA, File.read(sample[:path]), languages)
          assert_equal language.name, results.first[0], "#{sample[:path]}
#{results.inspect}"
        end
        """
        pass


if __name__ == '__main__':
    main()