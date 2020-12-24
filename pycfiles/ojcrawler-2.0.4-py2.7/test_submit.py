# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ojcrawler/tests/test_submit.py
# Compiled at: 2018-12-29 12:55:58
from ojcrawler.control import Controller
import json, unittest, os
data = json.load(open(os.path.join(os.getcwd(), 'accounts.json')))

class Test(unittest.TestCase):

    def setUp(self):
        self.ctl = Controller()
        for oj_name in data:
            self.ctl.update_account(oj_name, data[oj_name]['handle'], data[oj_name]['password'])

    def test_submit(self):
        pass

    def test_crawler_hdu(self):
        pid = 1000
        lang = 'g++'
        ac_src = '\n        #include<bits/stdc++.h>\n        using namespace std;\n        int main()\n        {\n            int a,b;\n            while(cin>>a>>b)cout<<a+b<<endl;\n            return 0;\n        }\n        '
        wa_src = '\n        #include<bits/stdc++.h>\n        using namespace std;\n        int main()\n        {\n            int a,b;\n            while(cin>>a>>b)cout<<a-b<<endl;\n            return 0;\n        }\n        '
        self.ctl.submit_code('hdu', ac_src, lang, pid)
        self.ctl.submit_code('hdu', wa_src, lang, pid)

    def test_crawler_poj(self):
        pid = 1000
        lang = 'g++'
        wa_src = '\n        #include<iostream>\n        using namespace std;\n        int main()\n        {\n            int a,b;\n            while(cin>>a>>b)cout<<a-b<<endl;\n            return 0;\n        }\n        '
        ac_src = '\n        #include<iostream>\n        using namespace std;\n        int main()\n        {\n            int a,b;\n            while(cin>>a>>b)cout<<a+b<<endl;\n            return 0;\n        }\n        '
        self.ctl.submit_code('poj', ac_src, lang, pid)
        self.ctl.submit_code('poj', wa_src, lang, pid)

    def test_crawler_cf(self):
        pid = '1A'
        lang = 'GNU G++11 5.1.0'
        src = '\n        #include <iostream>\n        using namespace std;\n        int n,m,a;\n        long long x,y;\n        hello ce\n        int main() {\n            cin>>n>>m>>a;\n            x=n/a+(n%a==0?0:1);\n            y=m/a+(m%a==0?0:1);\n            cout<<x*y<<endl;\n            return 0;\n        }\n        '
        self.ctl.submit_code('codeforces', src, lang, pid)


if __name__ == '__main__':
    unittest.main()