# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/tests/test_minifier.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import unittest
from slimit import minify

class MinifierTestCase(unittest.TestCase):

    def assertMinified(self, source, expected):
        minified = minify(source)
        self.maxDiff = None
        self.assertSequenceEqual(minified, expected)
        return

    TEST_CASES = [
     ('\n        jQuery.fn = jQuery.prototype = {\n                // For internal use only.\n                _data: function( elem, name, data ) {\n                        return jQuery.data( elem, name, data, true );\n                }\n        };\n        ',
 'jQuery.fn=jQuery.prototype={_data:function(elem,name,data){return jQuery.data(elem,name,data,true);}};'),
     ('context = context instanceof jQuery ? context[0] : context;', 'context=context instanceof jQuery?context[0]:context;'),
     ("\n        /*\n        * A number of helper functions used for managing events.\n        * Many of the ideas behind this code originated from\n        * Dean Edwards' addEvent library.\n        */\n        if ( elem && elem.parentNode ) {\n                // Handle the case where IE and Opera return items\n                // by name instead of ID\n                if ( elem.id !== match[2] ) {\n                        return rootjQuery.find( selector );\n                }\n\n                // Otherwise, we inject the element directly into the jQuery object\n                this.length = 1;\n                this[0] = elem;\n        }\n        ",
 'if(elem&&elem.parentNode){if(elem.id!==match[2])return rootjQuery.find(selector);this.length=1;this[0]=elem;}'),
     ('\n        var a = function( obj ) {\n                for ( var name in obj ) {\n                        return false;\n                }\n                return true;\n        };\n        ',
 'var a=function(obj){for(var name in obj)return false;return true;};'),
     ('\n        x = "string", y = 5;\n\n        (x = 5) ? true : false;\n\n        for (p in obj)\n        ;\n\n        if (true)\n          val = null;\n        else\n          val = false;\n\n        ',
 'x="string",y=5;(x=5)?true:false;for(p in obj);if(true)val=null;else val=false;'),
     ('\n        for (x = 0; true; x++)\n        ;\n        for (; true; x++)\n        ;\n        for (x = 0, y = 5; true; x++)\n        ;\n\n        y = (x + 5) * 20;\n\n        ',
 'for(x=0;true;x++);for(;true;x++);for(x=0,y=5;true;x++);y=(x+5)*20;'),
     ('\n        delete x;\n        typeof x;\n        void x;\n        x += (!y)++;\n        ',
 'delete x;typeof x;void x;x+=(!y)++;'),
     ('\n        label:\n        if ( i == 0 )\n          continue label;\n        switch (day) {\n        case 5:\n          break ;\n        default:\n          break label;\n        }\n        ',
 'label:if(i==0)continue label;switch(day){case 5:break;default:break label;}'),
     ('\n        while (i <= 7) {\n          if ( i == 3 )\n              continue;\n          if ( i == 0 )\n              break;\n        }\n        ',
 'while(i<=7){if(i==3)continue;if(i==0)break;}'),
     ('\n        function a(x, y) {\n         var re = /ab+c/;\n         if (x == 1)\n           return x + y;\n         if (x == 3)\n           return {x: 1};\n         else\n           return;\n        }\n        ',
 'function a(x,y){var re=/ab+c/;if(x==1)return x+y;if(x==3)return{x:1};else return;}'),
     ('return new jQuery.fn.init( selector, context, rootjQuery );', 'return new jQuery.fn.init(selector,context,rootjQuery);'),
     ('\n        if (true) {\n          x = true;\n          y = 3;\n        } else {\n          x = false\n          y = 5\n        }\n        ',
 'if(true){x=true;y=3;}else{x=false;y=5;}'),
     ("\n        if (true) {\n          x = true;\n          y = 3;\n        } else\n          (x + ' qw').split(' ');\n        ",
 "if(true){x=true;y=3;}else(x+' qw').split(' ');"),
     ('do { x += 1; } while(true);', 'do x+=1;while(true);'),
     ('do { x += 1; y += 1;} while(true);', 'do{x+=1;y+=1;}while(true);'),
     ('var a = [1, 2, 3, ,,,5];', 'var a=[1,2,3,,,,5];'),
     ('\n        with (obj) {\n          a = b;\n        }\n        ', 'with(obj)a=b;'),
     ('\n        with (obj) {\n          a = b;\n          c = d;\n        }\n        ',
 'with(obj){a=b;c=d;}'),
     ('\n        if (true) {\n          x = true;\n        } else {\n          x = false\n        }\n        ',
 'if(true)x=true;else x=false;'),
     ('\n        if (true) {\n          x = true;\n          y = false;\n        } else {\n          x = false;\n          y = true;\n        }\n        ',
 'if(true){x=true;y=false;}else{x=false;y=true;}'),
     ('\n        try {\n          throw "my_exception"; // generates an exception\n        }\n        catch (e) {\n          // statements to handle any exceptions\n          log(e); // pass exception object to error handler\n        }\n        finally {\n          closefiles(); // always close the resource\n        }\n        ',
 'try{throw "my_exception";}catch(e){log(e);}finally{closefiles();}'),
     ('\n        try {\n        }\n        catch (e) {\n        }\n        finally {\n        }\n        ',
 'try{}catch(e){}finally{}'),
     ("\n        try {\n          x = 3;\n          y = 5;\n        }\n        catch (e) {\n          log(e);\n          log('e');\n        }\n        finally {\n          z = 7;\n          log('z');\n        }\n        ",
 "try{x=3;y=5;}catch(e){log(e);log('e');}finally{z=7;log('z');}"),
     ('\n        if ( obj ) {\n                for ( n in obj ) {\n                        if ( v === false) {\n                                break;\n                        }\n                }\n        } else {\n                for ( ; i < l; ) {\n                        if ( nv === false ) {\n                                break;\n                        }\n                }\n        }\n        ',
 'if(obj){for(n in obj)if(v===false)break;}else for(;i<l;)if(nv===false)break;'),
     ('\n        if ( obj ) {\n                for ( n in obj ) {\n                        if ( v === false) {\n                                break;\n                        }\n                }\n                x = 5;\n        } else {\n                for ( ; i < l; ) {\n                        if ( nv === false ) {\n                                break;\n                        }\n                }\n        }\n        ',
 'if(obj){for(n in obj)if(v===false)break;x=5;}else for(;i<l;)if(nv===false)break;'),
     ('\n        if ( obj ) {\n                for ( n in obj ) {\n                        if ( v === false) {\n                                break;\n                        } else {\n                                n = 3;\n                        }\n                }\n        } else {\n                for ( ; i < l; ) {\n                        if ( nv === false ) {\n                                break;\n                        }\n                }\n        }\n        ',
 'if(obj)for(n in obj)if(v===false)break;else n=3;else for(;i<l;)if(nv===false)break;'),
     ('foo["bar"];', 'foo.bar;'),
     ("foo['bar'];", 'foo.bar;'),
     ('foo[\'bar"\']=42;', 'foo[\'bar"\']=42;'),
     ('foo["bar\'"]=42;', 'foo["bar\'"]=42;'),
     ('foo["bar bar"];', 'foo["bar bar"];'),
     ('foo["bar"+"bar"];', 'foo["bar"+"bar"];'),
     ('foo["for"];', 'foo["for"];'),
     ('foo["class"];', 'foo["class"];'),
     ('c||(c=393);', 'c||(c=393);'),
     ('c||(c=393,a=323,b=2321);', 'c||(c=393,a=323,b=2321);'),
     ('for(a?b:c;d;)e=1;', 'for(a?b:c;d;)e=1;'),
     ('"begin"+ ++a+"end";', '"begin"+ ++a+"end";'),
     ("\n         (function($) {\n             $.hello = 'world';\n         }(jQuery));\n         ",
 "(function($){$.hello='world';}(jQuery));"),
     ('for(o(); i < 3; i++) {}', 'for(o();i<3;i++){}'),
     ('for(i++; i < 3; i++) {}', 'for(i++;i<3;i++){}'),
     ('for(i--; i < 3; i++) {}', 'for(i--;i<3;i++){}'),
     ('for(i; i < 3; i++) {}', 'for(i;i<3;i++){}'),
     ('\n         Name.prototype = {\n           getPageProp: function Page_getPageProp(key) {\n             return this.pageDict.get(key);\n           },\n\n           get fullName() {\n             return this.first + " " + this.last;\n           },\n\n           set fullName(name) {\n             var names = name.split(" ");\n             this.first = names[0];\n             this.last = names[1];\n           }\n         };\n         ',
 'Name.prototype={getPageProp:function Page_getPageProp(key){return this.pageDict.get(key);},get fullName(){return this.first+" "+this.last;},set fullName(name){var names=name.split(" ");this.first=names[0];this.last=names[1];}};')]


def make_test_function(input, expected):

    def test_func(self):
        self.assertMinified(input, expected)

    return test_func


for index, (input, expected) in enumerate(MinifierTestCase.TEST_CASES):
    func = make_test_function(input, expected)
    setattr(MinifierTestCase, 'test_case_%d' % index, func)