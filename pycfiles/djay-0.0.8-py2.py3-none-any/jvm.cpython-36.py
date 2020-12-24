# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/jvm.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 69967 bytes
"""
    pygments.lexers.jvm
    ~~~~~~~~~~~~~~~~~~~

    Pygments lexers for JVM languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, this, combined, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
from pygments.util import shebang_matches
from pygments import unistring as uni
__all__ = [
 'JavaLexer', 'ScalaLexer', 'GosuLexer', 'GosuTemplateLexer',
 'GroovyLexer', 'IokeLexer', 'ClojureLexer', 'ClojureScriptLexer',
 'KotlinLexer', 'XtendLexer', 'AspectJLexer', 'CeylonLexer',
 'PigLexer', 'GoloLexer', 'JasminLexer', 'SarlLexer']

class JavaLexer(RegexLexer):
    __doc__ = '\n    For `Java <http://www.sun.com/java/>`_ source code.\n    '
    name = 'Java'
    aliases = ['java']
    filenames = ['*.java']
    mimetypes = ['text/x-java']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE
    tokens = {'root':[
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '(assert|break|case|catch|continue|default|do|else|finally|for|if|goto|instanceof|new|return|switch|this|throw|try|while)\\b',
       Keyword),
      (
       '((?:(?:[^\\W\\d]|\\$)[\\w.\\[\\]$<>]*\\s+)+?)((?:[^\\W\\d]|\\$)[\\w$]*)(\\s*)(\\()',
       bygroups(using(this), Name.Function, Text, Operator)),
      (
       '@[^\\W\\d][\\w.]*', Name.Decorator),
      (
       '(abstract|const|enum|extends|final|implements|native|private|protected|public|static|strictfp|super|synchronized|throws|transient|volatile)\\b',
       Keyword.Declaration),
      (
       '(boolean|byte|char|double|float|int|long|short|void)\\b',
       Keyword.Type),
      (
       '(package)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
      (
       '(true|false|null)\\b', Keyword.Constant),
      (
       '(class|interface)(\\s+)', bygroups(Keyword.Declaration, Text),
       'class'),
      (
       '(import(?:\\s+static)?)(\\s+)', bygroups(Keyword.Namespace, Text),
       'import'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-fA-F]{4}'", String.Char),
      (
       '(\\.)((?:[^\\W\\d]|\\$)[\\w$]*)', bygroups(Operator, Name.Attribute)),
      (
       '^\\s*([^\\W\\d]|\\$)[\\w$]*:', Name.Label),
      (
       '([^\\W\\d]|\\$)[\\w$]*', Name),
      (
       '([0-9][0-9_]*\\.([0-9][0-9_]*)?|\\.[0-9][0-9_]*)([eE][+\\-]?[0-9][0-9_]*)?[fFdD]?|[0-9][eE][+\\-]?[0-9][0-9_]*[fFdD]?|[0-9]([eE][+\\-]?[0-9][0-9_]*)?[fFdD]|0[xX]([0-9a-fA-F][0-9a-fA-F_]*\\.?|([0-9a-fA-F][0-9a-fA-F_]*)?\\.[0-9a-fA-F][0-9a-fA-F_]*)[pP][+\\-]?[0-9][0-9_]*[fFdD]?',
       Number.Float),
      (
       '0[xX][0-9a-fA-F][0-9a-fA-F_]*[lL]?', Number.Hex),
      (
       '0[bB][01][01_]*[lL]?', Number.Bin),
      (
       '0[0-7_]+[lL]?', Number.Oct),
      (
       '0|[1-9][0-9_]*[lL]?', Number.Integer),
      (
       '[~^*!%&\\[\\](){}<>|+=:;,./?-]', Operator),
      (
       '\\n', Text)], 
     'class':[
      (
       '([^\\W\\d]|\\$)[\\w$]*', Name.Class, '#pop')], 
     'import':[
      (
       '[\\w.]+\\*?', Name.Namespace, '#pop')]}


class AspectJLexer(JavaLexer):
    __doc__ = '\n    For `AspectJ <http://www.eclipse.org/aspectj/>`_ source code.\n\n    .. versionadded:: 1.6\n    '
    name = 'AspectJ'
    aliases = ['aspectj']
    filenames = ['*.aj']
    mimetypes = ['text/x-aspectj']
    aj_keywords = set(('aspect', 'pointcut', 'privileged', 'call', 'execution', 'initialization',
                       'preinitialization', 'handler', 'get', 'set', 'staticinitialization',
                       'target', 'args', 'within', 'withincode', 'cflow', 'cflowbelow',
                       'annotation', 'before', 'after', 'around', 'proceed', 'throwing',
                       'returning', 'adviceexecution', 'declare', 'parents', 'warning',
                       'error', 'soft', 'precedence', 'thisJoinPoint', 'thisJoinPointStaticPart',
                       'thisEnclosingJoinPointStaticPart', 'issingleton', 'perthis',
                       'pertarget', 'percflow', 'percflowbelow', 'pertypewithin',
                       'lock', 'unlock', 'thisAspectInstance'))
    aj_inter_type = set(('parents:', 'warning:', 'error:', 'soft:', 'precedence:'))
    aj_inter_type_annotation = set(('@type', '@method', '@constructor', '@field'))

    def get_tokens_unprocessed(self, text):
        for index, token, value in JavaLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.aj_keywords:
                yield (
                 index, Keyword, value)
            elif token is Name.Label and value in self.aj_inter_type:
                yield (
                 index, Keyword, value[:-1])
                yield (index, Operator, value[(-1)])
            elif token is Name.Decorator and value in self.aj_inter_type_annotation:
                yield (
                 index, Keyword, value)
            else:
                yield (
                 index, token, value)


class ScalaLexer(RegexLexer):
    __doc__ = '\n    For `Scala <http://www.scala-lang.org>`_ source code.\n    '
    name = 'Scala'
    aliases = ['scala']
    filenames = ['*.scala']
    mimetypes = ['text/x-scala']
    flags = re.MULTILINE | re.DOTALL
    op = '[-~\\^\\*!%&\\\\<>\\|+=:/?@¦-§©¬®°-±¶×÷϶҂؆-؈؎-؏۩۽-۾߶৺୰௳-௸௺౿ೱ-ೲ൹༁-༃༓-༗༚-༟༴༶༸྾-࿅࿇-࿏႞-႟፠᎐-᎙᥀᧠-᧿᭡-᭪᭴-᭼⁄⁒⁺-⁼₊-₌℀-℁℃-℆℈-℉℔№-℘℞-℣℥℧℩℮℺-℻⅀-⅄⅊-⅍⅏←-⌨⌫-⑊⒜-ⓩ─-❧➔-⟄⟇-⟥⟰-⦂⦙-⧗⧜-⧻⧾-⭔⳥-⳪⺀-⿻〄〒-〓〠〶-〷〾-〿㆐-㆑㆖-㆟㇀-㇣㈀-㈞㈪-㉐㉠-㉿㊊-㊰㋀-㏿䷀-䷿꒐-꓆꠨-꠫﬩﷽﹢﹤-﹦＋＜-＞｜～￢￤￨-￮￼-�]+'
    letter = '[a-zA-Z\\$_ªµºÀ-ÖØ-öø-ʯͰ-ͳͶ-ͷͻ-ͽΆΈ-ϵϷ-ҁҊ-Ֆա-ևא-ײء-ؿف-يٮ-ٯٱ-ۓەۮ-ۯۺ-ۼۿܐܒ-ܯݍ-ޥޱߊ-ߪऄ-हऽॐक़-ॡॲ-ॿঅ-হঽৎড়-ৡৰ-ৱਅ-ਹਖ਼-ਫ਼ੲ-ੴઅ-હઽૐ-ૡଅ-ହଽଡ଼-ୡୱஃ-ஹௐఅ-ఽౘ-ౡಅ-ಹಽೞ-ೡഅ-ഽൠ-ൡൺ-ൿඅ-ෆก-ะา-ำเ-ๅກ-ະາ-ຳຽ-ໄໜ-ༀཀ-ཬྈ-ྋက-ဪဿၐ-ၕၚ-ၝၡၥ-ၦၮ-ၰၵ-ႁႎႠ-ჺᄀ-ፚᎀ-ᎏᎠ-ᙬᙯ-ᙶᚁ-ᚚᚠ-ᛪᛮ-ᜑᜠ-ᜱᝀ-ᝑᝠ-ᝰក-ឳៜᠠ-ᡂᡄ-ᢨᢪ-ᤜᥐ-ᦩᧁ-ᧇᨀ-ᨖᬅ-ᬳᭅ-ᭋᮃ-ᮠᮮ-ᮯᰀ-ᰣᱍ-ᱏᱚ-ᱷᴀ-ᴫᵢ-ᵷᵹ-ᶚḀ-ᾼιῂ-ῌῐ-Ίῠ-Ῥῲ-ῼⁱⁿℂℇℊ-ℓℕℙ-ℝℤΩℨK-ℭℯ-ℹℼ-ℿⅅ-ⅉⅎⅠ-ↈⰀ-ⱼⲀ-ⳤⴀ-ⵥⶀ-ⷞ〆-〇〡-〩〸-〺〼ぁ-ゖゟァ-ヺヿ-ㆎㆠ-ㆷㇰ-ㇿ㐀-䶵一-ꀔꀖ-ꒌꔀ-ꘋꘐ-ꘟꘪ-ꙮꚀ-ꚗꜢ-ꝯꝱ-ꞇꞋ-ꠁꠃ-ꠅꠇ-ꠊꠌ-ꠢꡀ-ꡳꢂ-ꢳꤊ-ꤥꤰ-ꥆꨀ-ꨨꩀ-ꩂꩄ-ꩋ가-힣豈-יִײַ-ﬨשׁ-ﴽﵐ-ﷻﹰ-ﻼＡ-Ｚａ-ｚｦ-ｯｱ-ﾝﾠ-ￜ]'
    upper = '[A-Z\\$_À-ÖØ-ÞĀĂĄĆĈĊČĎĐĒĔĖĘĚĜĞĠĢĤĦĨĪĬĮİĲĴĶĹĻĽĿŁŃŅŇŊŌŎŐŒŔŖŘŚŜŞŠŢŤŦŨŪŬŮŰŲŴŶŸ-ŹŻŽƁ-ƂƄƆ-ƇƉ-ƋƎ-ƑƓ-ƔƖ-ƘƜ-ƝƟ-ƠƢƤƦ-ƧƩƬƮ-ƯƱ-ƳƵƷ-ƸƼǄǇǊǍǏǑǓǕǗǙǛǞǠǢǤǦǨǪǬǮǱǴǶ-ǸǺǼǾȀȂȄȆȈȊȌȎȐȒȔȖȘȚȜȞȠȢȤȦȨȪȬȮȰȲȺ-ȻȽ-ȾɁɃ-ɆɈɊɌɎͰͲͶΆΈ-ΏΑ-ΫϏϒ-ϔϘϚϜϞϠϢϤϦϨϪϬϮϴϷϹ-ϺϽ-ЯѠѢѤѦѨѪѬѮѰѲѴѶѸѺѼѾҀҊҌҎҐҒҔҖҘҚҜҞҠҢҤҦҨҪҬҮҰҲҴҶҸҺҼҾӀ-ӁӃӅӇӉӋӍӐӒӔӖӘӚӜӞӠӢӤӦӨӪӬӮӰӲӴӶӸӺӼӾԀԂԄԆԈԊԌԎԐԒԔԖԘԚԜԞԠԢԱ-ՖႠ-ჅḀḂḄḆḈḊḌḎḐḒḔḖḘḚḜḞḠḢḤḦḨḪḬḮḰḲḴḶḸḺḼḾṀṂṄṆṈṊṌṎṐṒṔṖṘṚṜṞṠṢṤṦṨṪṬṮṰṲṴṶṸṺṼṾẀẂẄẆẈẊẌẎẐẒẔẞẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸỺỼỾἈ-ἏἘ-ἝἨ-ἯἸ-ἿὈ-ὍὙ-ὟὨ-ὯᾸ-ΆῈ-ΉῘ-ΊῨ-ῬῸ-Ώℂℇℋ-ℍℐ-ℒℕℙ-ℝℤΩℨK-ℭℰ-ℳℾ-ℿⅅↃⰀ-ⰮⱠⱢ-ⱤⱧⱩⱫⱭ-ⱯⱲⱵⲀⲂⲄⲆⲈⲊⲌⲎⲐⲒⲔⲖⲘⲚⲜⲞⲠⲢⲤⲦⲨⲪⲬⲮⲰⲲⲴⲶⲸⲺⲼⲾⳀⳂⳄⳆⳈⳊⳌⳎⳐⳒⳔⳖⳘⳚⳜⳞⳠⳢꙀꙂꙄꙆꙈꙊꙌꙎꙐꙒꙔꙖꙘꙚꙜꙞꙢꙤꙦꙨꙪꙬꚀꚂꚄꚆꚈꚊꚌꚎꚐꚒꚔꚖꜢꜤꜦꜨꜪꜬꜮꜲꜴꜶꜸꜺꜼꜾꝀꝂꝄꝆꝈꝊꝌꝎꝐꝒꝔꝖꝘꝚꝜꝞꝠꝢꝤꝦꝨꝪꝬꝮꝹꝻꝽ-ꝾꞀꞂꞄꞆꞋＡ-Ｚ]'
    idrest = '%s(?:%s|[0-9])*(?:(?<=_)%s)?' % (letter, letter, op)
    letter_letter_digit = '%s(?:%s|\\d)*' % (letter, letter)
    tokens = {'root':[
      (
       '(class|trait|object)(\\s+)', bygroups(Keyword, Text), 'class'),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       '@%s' % idrest, Name.Decorator),
      (
       '(abstract|ca(?:se|tch)|d(?:ef|o)|e(?:lse|xtends)|f(?:inal(?:ly)?|or(?:Some)?)|i(?:f|mplicit)|lazy|match|new|override|pr(?:ivate|otected)|re(?:quires|turn)|s(?:ealed|uper)|t(?:h(?:is|row)|ry)|va[lr]|w(?:hile|ith)|yield)\\b|(<[%:-]|=>|>:|[#=@_⇒←])(\\b|(?=\\s)|$)',
       Keyword),
      (
       ':(?!%s)' % op, Keyword, 'type'),
      (
       '%s%s\\b' % (upper, idrest), Name.Class),
      (
       '(true|false|null)\\b', Keyword.Constant),
      (
       '(import|package)(\\s+)', bygroups(Keyword, Text), 'import'),
      (
       '(type)(\\s+)', bygroups(Keyword, Text), 'type'),
      (
       '""".*?"""(?!")', String),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-fA-F]{4}'", String.Char),
      (
       "'%s" % idrest, Text.Symbol),
      (
       '[fs]"""', String, 'interptriplestring'),
      (
       '[fs]"', String, 'interpstring'),
      (
       'raw"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       idrest, Name),
      (
       '`[^`]+`', Name),
      (
       '\\[', Operator, 'typeparam'),
      (
       '[(){};,.#]', Operator),
      (
       op, Operator),
      (
       '([0-9][0-9]*\\.[0-9]*|\\.[0-9]+)([eE][+-]?[0-9]+)?[fFdD]?',
       Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+L?', Number.Integer),
      (
       '\\n', Text)], 
     'class':[
      (
       '(%s|%s|`[^`]+`)(\\s*)(\\[)' % (idrest, op),
       bygroups(Name.Class, Text, Operator), 'typeparam'),
      (
       '\\s+', Text),
      (
       '\\{', Operator, '#pop'),
      (
       '\\(', Operator, '#pop'),
      (
       '//.*?\\n', Comment.Single, '#pop'),
      (
       '%s|%s|`[^`]+`' % (idrest, op), Name.Class, '#pop')], 
     'type':[
      (
       '\\s+', Text),
      (
       '<[%:]|>:|[#_]|forSome|type', Keyword),
      (
       '([,);}]|=>|=|⇒)(\\s*)', bygroups(Operator, Text), '#pop'),
      (
       '[({]', Operator, '#push'),
      (
       '((?:%s|%s|`[^`]+`)(?:\\.(?:%s|%s|`[^`]+`))*)(\\s*)(\\[)' % (
        idrest, op, idrest, op),
       bygroups(Keyword.Type, Text, Operator), ('#pop', 'typeparam')),
      (
       '((?:%s|%s|`[^`]+`)(?:\\.(?:%s|%s|`[^`]+`))*)(\\s*)$' % (
        idrest, op, idrest, op),
       bygroups(Keyword.Type, Text), '#pop'),
      (
       '//.*?\\n', Comment.Single, '#pop'),
      (
       '\\.|%s|%s|`[^`]+`' % (idrest, op), Keyword.Type)], 
     'typeparam':[
      (
       '[\\s,]+', Text),
      (
       '<[%:]|=>|>:|[#_⇒]|forSome|type', Keyword),
      (
       '([\\])}])', Operator, '#pop'),
      (
       '[(\\[{]', Operator, '#push'),
      (
       '\\.|%s|%s|`[^`]+`' % (idrest, op), Keyword.Type)], 
     'comment':[
      (
       '[^/*]+', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'import':[
      (
       '(%s|\\.)+' % idrest, Name.Namespace, '#pop')], 
     'interpstringcommon':[
      (
       '[^"$\\\\]+', String),
      (
       '\\$\\$', String),
      (
       '\\$' + letter_letter_digit, String.Interpol),
      (
       '\\$\\{', String.Interpol, 'interpbrace'),
      (
       '\\\\.', String)], 
     'interptriplestring':[
      (
       '"""(?!")', String, '#pop'),
      (
       '"', String),
      include('interpstringcommon')], 
     'interpstring':[
      (
       '"', String, '#pop'),
      include('interpstringcommon')], 
     'interpbrace':[
      (
       '\\}', String.Interpol, '#pop'),
      (
       '\\{', String.Interpol, '#push'),
      include('root')]}


class GosuLexer(RegexLexer):
    __doc__ = '\n    For Gosu source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'Gosu'
    aliases = ['gosu']
    filenames = ['*.gs', '*.gsx', '*.gsp', '*.vark']
    mimetypes = ['text/x-gosu']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root':[
      (
       '^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()',
       bygroups(using(this), Name.Function, Text, Operator)),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '@[a-zA-Z_][\\w.]*', Name.Decorator),
      (
       '(in|as|typeof|statictypeof|typeis|typeas|if|else|foreach|for|index|while|do|continue|break|return|try|catch|finally|this|throw|new|switch|case|default|eval|super|outer|classpath|using)\\b',
       Keyword),
      (
       '(var|delegate|construct|function|private|internal|protected|public|abstract|override|final|static|extends|transient|implements|represents|readonly)\\b',
       Keyword.Declaration),
      (
       '(property\\s+)(get|set)?', Keyword.Declaration),
      (
       '(boolean|byte|char|double|float|int|long|short|void|block)\\b',
       Keyword.Type),
      (
       '(package)(\\s+)', bygroups(Keyword.Namespace, Text)),
      (
       '(true|false|null|NaN|Infinity)\\b', Keyword.Constant),
      (
       '(class|interface|enhancement|enum)(\\s+)([a-zA-Z_]\\w*)',
       bygroups(Keyword.Declaration, Text, Name.Class)),
      (
       '(uses)(\\s+)([\\w.]+\\*?)',
       bygroups(Keyword.Namespace, Text, Name.Namespace)),
      (
       '"', String, 'string'),
      (
       '(\\??[.#])([a-zA-Z_]\\w*)',
       bygroups(Operator, Name.Attribute)),
      (
       '(:)([a-zA-Z_]\\w*)',
       bygroups(Operator, Name.Attribute)),
      (
       '[a-zA-Z_$]\\w*', Name),
      (
       'and|or|not|[\\\\~^*!%&\\[\\](){}<>|+=:;,./?-]', Operator),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '[0-9]+', Number.Integer),
      (
       '\\n', Text)], 
     'templateText':[
      (
       '(\\\\<)|(\\\\\\$)', String),
      (
       '(<%@\\s+)(extends|params)',
       bygroups(Operator, Name.Decorator), 'stringTemplate'),
      (
       '<%!--.*?--%>', Comment.Multiline),
      (
       '(<%)|(<%=)', Operator, 'stringTemplate'),
      (
       '\\$\\{', Operator, 'stringTemplateShorthand'),
      (
       '.', String)], 
     'string':[
      (
       '"', String, '#pop'),
      include('templateText')], 
     'stringTemplate':[
      (
       '"', String, 'string'),
      (
       '%>', Operator, '#pop'),
      include('root')], 
     'stringTemplateShorthand':[
      (
       '"', String, 'string'),
      (
       '\\{', Operator, 'stringTemplateShorthand'),
      (
       '\\}', Operator, '#pop'),
      include('root')]}


class GosuTemplateLexer(Lexer):
    __doc__ = '\n    For Gosu templates.\n\n    .. versionadded:: 1.5\n    '
    name = 'Gosu Template'
    aliases = ['gst']
    filenames = ['*.gst']
    mimetypes = ['text/x-gosu-template']

    def get_tokens_unprocessed(self, text):
        lexer = GosuLexer()
        stack = ['templateText']
        for item in lexer.get_tokens_unprocessed(text, stack):
            yield item


class GroovyLexer(RegexLexer):
    __doc__ = '\n    For `Groovy <http://groovy.codehaus.org/>`_ source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'Groovy'
    aliases = ['groovy']
    filenames = ['*.groovy', '*.gradle']
    mimetypes = ['text/x-groovy']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root':[
      (
       '#!(.*?)$', Comment.Preproc, 'base'),
      default('base')], 
     'base':[
      (
       '^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()',
       bygroups(using(this), Name.Function, Text, Operator)),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '@[a-zA-Z_][\\w.]*', Name.Decorator),
      (
       '(assert|break|case|catch|continue|default|do|else|finally|for|if|goto|instanceof|new|return|switch|this|throw|try|while|in|as)\\b',
       Keyword),
      (
       '(abstract|const|enum|extends|final|implements|native|private|protected|public|static|strictfp|super|synchronized|throws|transient|volatile)\\b',
       Keyword.Declaration),
      (
       '(def|boolean|byte|char|double|float|int|long|short|void)\\b',
       Keyword.Type),
      (
       '(package)(\\s+)', bygroups(Keyword.Namespace, Text)),
      (
       '(true|false|null)\\b', Keyword.Constant),
      (
       '(class|interface)(\\s+)', bygroups(Keyword.Declaration, Text),
       'class'),
      (
       '(import)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
      (
       '""".*?"""', String.Double),
      (
       "'''.*?'''", String.Single),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
      (
       '\\$/((?!/\\$).)*/\\$', String),
      (
       '/(\\\\\\\\|\\\\"|[^/])*/', String),
      (
       "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-fA-F]{4}'", String.Char),
      (
       '(\\.)([a-zA-Z_]\\w*)', bygroups(Operator, Name.Attribute)),
      (
       '[a-zA-Z_]\\w*:', Name.Label),
      (
       '[a-zA-Z_$]\\w*', Name),
      (
       '[~^*!%&\\[\\](){}<>|+=:;,./?-]', Operator),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+L?', Number.Integer),
      (
       '\\n', Text)], 
     'class':[
      (
       '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     'import':[
      (
       '[\\w.]+\\*?', Name.Namespace, '#pop')]}

    def analyse_text(text):
        return shebang_matches(text, 'groovy')


class IokeLexer(RegexLexer):
    __doc__ = '\n    For `Ioke <http://ioke.org/>`_ (a strongly typed, dynamic,\n    prototype based programming language) source.\n\n    .. versionadded:: 1.4\n    '
    name = 'Ioke'
    filenames = ['*.ik']
    aliases = ['ioke', 'ik']
    mimetypes = ['text/x-iokesrc']
    tokens = {'interpolatableText':[
      (
       '(\\\\b|\\\\e|\\\\t|\\\\n|\\\\f|\\\\r|\\\\"|\\\\\\\\|\\\\#|\\\\\\Z|\\\\u[0-9a-fA-F]{1,4}|\\\\[0-3]?[0-7]?[0-7])',
       String.Escape),
      (
       '#\\{', Punctuation, 'textInterpolationRoot')], 
     'text':[
      (
       '(?<!\\\\)"', String, '#pop'),
      include('interpolatableText'),
      (
       '[^"]', String)], 
     'documentation':[
      (
       '(?<!\\\\)"', String.Doc, '#pop'),
      include('interpolatableText'),
      (
       '[^"]', String.Doc)], 
     'textInterpolationRoot':[
      (
       '\\}', Punctuation, '#pop'),
      include('root')], 
     'slashRegexp':[
      (
       '(?<!\\\\)/[im-psux]*', String.Regex, '#pop'),
      include('interpolatableText'),
      (
       '\\\\/', String.Regex),
      (
       '[^/]', String.Regex)], 
     'squareRegexp':[
      (
       '(?<!\\\\)][im-psux]*', String.Regex, '#pop'),
      include('interpolatableText'),
      (
       '\\\\]', String.Regex),
      (
       '[^\\]]', String.Regex)], 
     'squareText':[
      (
       '(?<!\\\\)]', String, '#pop'),
      include('interpolatableText'),
      (
       '[^\\]]', String)], 
     'root':[
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       ';(.*?)\\n', Comment),
      (
       '\\A#!(.*?)\\n', Comment),
      (
       '#/', String.Regex, 'slashRegexp'),
      (
       '#r\\[', String.Regex, 'squareRegexp'),
      (
       ':[\\w!:?]+', String.Symbol),
      (
       '[\\w!:?]+:(?![\\w!?])', String.Other),
      (
       ':"(\\\\\\\\|\\\\"|[^"])*"', String.Symbol),
      (
       '((?<=fn\\()|(?<=fnx\\()|(?<=method\\()|(?<=macro\\()|(?<=lecro\\()|(?<=syntax\\()|(?<=dmacro\\()|(?<=dlecro\\()|(?<=dlecrox\\()|(?<=dsyntax\\())\\s*"',
       String.Doc, 'documentation'),
      (
       '"', String, 'text'),
      (
       '#\\[', String, 'squareText'),
      (
       '\\w[\\w!:?]+(?=\\s*=.*mimic\\s)', Name.Entity),
      (
       '[a-zA-Z_][\\w!:?]*(?=[\\s]*[+*/-]?=[^=].*($|\\.))',
       Name.Variable),
      (
       '(break|cond|continue|do|ensure|for|for:dict|for:set|if|let|loop|p:for|p:for:dict|p:for:set|return|unless|until|while|with)(?![\\w!:?])',
       Keyword.Reserved),
      (
       '(eval|mimic|print|println)(?![\\w!:?])', Keyword),
      (
       '(cell\\?|cellNames|cellOwner\\?|cellOwner|cells|cell|documentation|hash|identity|mimic|removeCell\\!|undefineCell\\!)(?![\\w!:?])',
       Keyword),
      (
       '(stackTraceAsText)(?![\\w!:?])', Keyword),
      (
       '(dict|list|message|set)(?![\\w!:?])', Keyword.Reserved),
      (
       '(case|case:and|case:else|case:nand|case:nor|case:not|case:or|case:otherwise|case:xor)(?![\\w!:?])',
       Keyword.Reserved),
      (
       '(asText|become\\!|derive|freeze\\!|frozen\\?|in\\?|is\\?|kind\\?|mimic\\!|mimics|mimics\\?|prependMimic\\!|removeAllMimics\\!|removeMimic\\!|same\\?|send|thaw\\!|uniqueHexId)(?![\\w!:?])',
       Keyword),
      (
       '(after|around|before)(?![\\w!:?])', Keyword.Reserved),
      (
       '(kind|cellDescriptionDict|cellSummary|genSym|inspect|notice)(?![\\w!:?])',
       Keyword),
      (
       '(use|destructuring)', Keyword.Reserved),
      (
       '(cell\\?|cellOwner\\?|cellOwner|cellNames|cells|cell|documentation|identity|removeCell!|undefineCell)(?![\\w!:?])',
       Keyword),
      (
       '(internal:compositeRegexp|internal:concatenateText|internal:createDecimal|internal:createNumber|internal:createRegexp|internal:createText)(?![\\w!:?])',
       Keyword.Reserved),
      (
       '(availableRestarts|bind|error\\!|findRestart|handle|invokeRestart|rescue|restart|signal\\!|warn\\!)(?![\\w!:?])',
       Keyword.Reserved),
      (
       '(nil|false|true)(?![\\w!:?])', Name.Constant),
      (
       '(Arity|Base|Call|Condition|DateTime|Aspects|Pointcut|Assignment|BaseBehavior|Boolean|Case|AndCombiner|Else|NAndCombiner|NOrCombiner|NotCombiner|OrCombiner|XOrCombiner|Conditions|Definitions|FlowControl|Internal|Literals|Reflection|DefaultMacro|DefaultMethod|DefaultSyntax|Dict|FileSystem|Ground|Handler|Hook|IO|IokeGround|Struct|LexicalBlock|LexicalMacro|List|Message|Method|Mixins|NativeMethod|Number|Origin|Pair|Range|Reflector|Regexp Match|Regexp|Rescue|Restart|Runtime|Sequence|Set|Symbol|System|Text|Tuple)(?![\\w!:?])',
       Name.Builtin),
      (
       '(generateMatchMethod|aliasMethod|λ|ʎ|fnx|fn|method|dmacro|dlecro|syntax|macro|dlecrox|lecrox|lecro|syntax)(?![\\w!:?])',
       Name.Function),
      (
       '-?0[xX][0-9a-fA-F]+', Number.Hex),
      (
       '-?(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
      (
       '-?\\d+', Number.Integer),
      (
       '#\\(', Punctuation),
      (
       '(&&>>|\\|\\|>>|\\*\\*>>|:::|::|\\.\\.\\.|===|\\*\\*>|\\*\\*=|&&>|&&=|\\|\\|>|\\|\\|=|\\->>|\\+>>|!>>|<>>>|<>>|&>>|%>>|#>>|@>>|/>>|\\*>>|\\?>>|\\|>>|\\^>>|~>>|\\$>>|=>>|<<=|>>=|<=>|<\\->|=~|!~|=>|\\+\\+|\\-\\-|<=|>=|==|!=|&&|\\.\\.|\\+=|\\-=|\\*=|\\/=|%=|&=|\\^=|\\|=|<\\-|\\+>|!>|<>|&>|%>|#>|\\@>|\\/>|\\*>|\\?>|\\|>|\\^>|~>|\\$>|<\\->|\\->|<<|>>|\\*\\*|\\?\\||\\?&|\\|\\||>|<|\\*|\\/|%|\\+|\\-|&|\\^|\\||=|\\$|!|~|\\?|#|≠|∘|∈|∉)',
       Operator),
      (
       '(and|nand|or|xor|nor|return|import)(?![\\w!?])',
       Operator),
      (
       "(\\`\\`|\\`|\\'\\'|\\'|\\.|\\,|@@|@|\\[|\\]|\\(|\\)|\\{|\\})", Punctuation),
      (
       '[A-Z][\\w!:?]*', Name.Class),
      (
       '[a-z_][\\w!:?]*', Name)]}


class ClojureLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Clojure <http://clojure.org/>`_ source code.\n\n    .. versionadded:: 0.11\n    '
    name = 'Clojure'
    aliases = ['clojure', 'clj']
    filenames = ['*.clj']
    mimetypes = ['text/x-clojure', 'application/x-clojure']
    special_forms = ('.', 'def', 'do', 'fn', 'if', 'let', 'new', 'quote', 'var', 'loop')
    declarations = ('def-', 'defn', 'defn-', 'defmacro', 'defmulti', 'defmethod', 'defstruct',
                    'defonce', 'declare', 'definline', 'definterface', 'defprotocol',
                    'defrecord', 'deftype', 'defproject', 'ns')
    builtins = ('*', '+', '-', '->', '/', '<', '<=', '=', '==', '>', '>=', '..', 'accessor',
                'agent', 'agent-errors', 'aget', 'alength', 'all-ns', 'alter', 'and',
                'append-child', 'apply', 'array-map', 'aset', 'aset-boolean', 'aset-byte',
                'aset-char', 'aset-double', 'aset-float', 'aset-int', 'aset-long',
                'aset-short', 'assert', 'assoc', 'await', 'await-for', 'bean', 'binding',
                'bit-and', 'bit-not', 'bit-or', 'bit-shift-left', 'bit-shift-right',
                'bit-xor', 'boolean', 'branch?', 'butlast', 'byte', 'cast', 'char',
                'children', 'class', 'clear-agent-errors', 'comment', 'commute',
                'comp', 'comparator', 'complement', 'concat', 'conj', 'cons', 'constantly',
                'cond', 'if-not', 'construct-proxy', 'contains?', 'count', 'create-ns',
                'create-struct', 'cycle', 'dec', 'deref', 'difference', 'disj', 'dissoc',
                'distinct', 'doall', 'doc', 'dorun', 'doseq', 'dosync', 'dotimes',
                'doto', 'double', 'down', 'drop', 'drop-while', 'edit', 'end?', 'ensure',
                'eval', 'every?', 'false?', 'ffirst', 'file-seq', 'filter', 'find',
                'find-doc', 'find-ns', 'find-var', 'first', 'float', 'flush', 'for',
                'fnseq', 'frest', 'gensym', 'get-proxy-class', 'get', 'hash-map',
                'hash-set', 'identical?', 'identity', 'if-let', 'import', 'in-ns',
                'inc', 'index', 'insert-child', 'insert-left', 'insert-right', 'inspect-table',
                'inspect-tree', 'instance?', 'int', 'interleave', 'intersection',
                'into', 'into-array', 'iterate', 'join', 'key', 'keys', 'keyword',
                'keyword?', 'last', 'lazy-cat', 'lazy-cons', 'left', 'lefts', 'line-seq',
                'list*', 'list', 'load', 'load-file', 'locking', 'long', 'loop',
                'macroexpand', 'macroexpand-1', 'make-array', 'make-node', 'map',
                'map-invert', 'map?', 'mapcat', 'max', 'max-key', 'memfn', 'merge',
                'merge-with', 'meta', 'min', 'min-key', 'name', 'namespace', 'neg?',
                'new', 'newline', 'next', 'nil?', 'node', 'not', 'not-any?', 'not-every?',
                'not=', 'ns-imports', 'ns-interns', 'ns-map', 'ns-name', 'ns-publics',
                'ns-refers', 'ns-resolve', 'ns-unmap', 'nth', 'nthrest', 'or', 'parse',
                'partial', 'path', 'peek', 'pop', 'pos?', 'pr', 'pr-str', 'print',
                'print-str', 'println', 'println-str', 'prn', 'prn-str', 'project',
                'proxy', 'proxy-mappings', 'quot', 'rand', 'rand-int', 'range', 're-find',
                're-groups', 're-matcher', 're-matches', 're-pattern', 're-seq',
                'read', 'read-line', 'reduce', 'ref', 'ref-set', 'refer', 'rem',
                'remove', 'remove-method', 'remove-ns', 'rename', 'rename-keys',
                'repeat', 'replace', 'replicate', 'resolve', 'rest', 'resultset-seq',
                'reverse', 'rfirst', 'right', 'rights', 'root', 'rrest', 'rseq',
                'second', 'select', 'select-keys', 'send', 'send-off', 'seq', 'seq-zip',
                'seq?', 'set', 'short', 'slurp', 'some', 'sort', 'sort-by', 'sorted-map',
                'sorted-map-by', 'sorted-set', 'special-symbol?', 'split-at', 'split-with',
                'str', 'string?', 'struct', 'struct-map', 'subs', 'subvec', 'symbol',
                'symbol?', 'sync', 'take', 'take-nth', 'take-while', 'test', 'time',
                'to-array', 'to-array-2d', 'tree-seq', 'true?', 'union', 'up', 'update-proxy',
                'val', 'vals', 'var-get', 'var-set', 'var?', 'vector', 'vector-zip',
                'vector?', 'when', 'when-first', 'when-let', 'when-not', 'with-local-vars',
                'with-meta', 'with-open', 'with-out-str', 'xml-seq', 'xml-zip', 'zero?',
                'zipmap', 'zipper')
    valid_name = '(?!#)[\\w!$%*+<=>?/.#|-]+'
    tokens = {'root': [
              (
               ';.*$', Comment.Single),
              (
               '[,\\s]+', Text),
              (
               '-?\\d+\\.\\d+', Number.Float),
              (
               '-?\\d+', Number.Integer),
              (
               '0x-?[abcdef\\d]+', Number.Hex),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "'" + valid_name, String.Symbol),
              (
               '\\\\(.|[a-z]+)', String.Char),
              (
               '::?#?' + valid_name, String.Symbol),
              (
               "~@|[`\\'#^~&@]", Operator),
              (
               words(special_forms, suffix=' '), Keyword),
              (
               words(declarations, suffix=' '), Keyword.Declaration),
              (
               words(builtins, suffix=' '), Name.Builtin),
              (
               '(?<=\\()' + valid_name, Name.Function),
              (
               valid_name, Name.Variable),
              (
               '(\\[|\\])', Punctuation),
              (
               '(\\{|\\})', Punctuation),
              (
               '(\\(|\\))', Punctuation)]}


class ClojureScriptLexer(ClojureLexer):
    __doc__ = '\n    Lexer for `ClojureScript <http://clojure.org/clojurescript>`_\n    source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'ClojureScript'
    aliases = ['clojurescript', 'cljs']
    filenames = ['*.cljs']
    mimetypes = ['text/x-clojurescript', 'application/x-clojurescript']


class TeaLangLexer(RegexLexer):
    __doc__ = '\n    For `Tea <http://teatrove.org/>`_ source code. Only used within a\n    TeaTemplateLexer.\n\n    .. versionadded:: 1.5\n    '
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root':[
      (
       '^(\\s*(?:[a-zA-Z_][\\w\\.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()',
       bygroups(using(this), Name.Function, Text, Operator)),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '@[a-zA-Z_][\\w\\.]*', Name.Decorator),
      (
       '(and|break|else|foreach|if|in|not|or|reverse)\\b',
       Keyword),
      (
       '(as|call|define)\\b', Keyword.Declaration),
      (
       '(true|false|null)\\b', Keyword.Constant),
      (
       '(template)(\\s+)', bygroups(Keyword.Declaration, Text), 'template'),
      (
       '(import)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "\\'(\\\\\\\\|\\\\\\'|[^\\'])*\\'", String),
      (
       '(\\.)([a-zA-Z_]\\w*)', bygroups(Operator, Name.Attribute)),
      (
       '[a-zA-Z_]\\w*:', Name.Label),
      (
       '[a-zA-Z_\\$]\\w*', Name),
      (
       '(isa|[.]{3}|[.]{2}|[=#!<>+-/%&;,.\\*\\\\\\(\\)\\[\\]\\{\\}])', Operator),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+L?', Number.Integer),
      (
       '\\n', Text)], 
     'template':[
      (
       '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     'import':[
      (
       '[\\w.]+\\*?', Name.Namespace, '#pop')]}


class CeylonLexer(RegexLexer):
    __doc__ = '\n    For `Ceylon <http://ceylon-lang.org/>`_ source code.\n\n    .. versionadded:: 1.6\n    '
    name = 'Ceylon'
    aliases = ['ceylon']
    filenames = ['*.ceylon']
    mimetypes = ['text/x-ceylon']
    flags = re.MULTILINE | re.DOTALL
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root':[
      (
       '^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()',
       bygroups(using(this), Name.Function, Text, Operator)),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       '(shared|abstract|formal|default|actual|variable|deprecated|small|late|literal|doc|by|see|throws|optional|license|tagged|final|native|annotation|sealed)\\b',
       Name.Decorator),
      (
       '(break|case|catch|continue|else|finally|for|in|if|return|switch|this|throw|try|while|is|exists|dynamic|nonempty|then|outer|assert|let)\\b',
       Keyword),
      (
       '(abstracts|extends|satisfies|super|given|of|out|assign)\\b',
       Keyword.Declaration),
      (
       '(function|value|void|new)\\b',
       Keyword.Type),
      (
       '(assembly|module|package)(\\s+)', bygroups(Keyword.Namespace, Text)),
      (
       '(true|false|null)\\b', Keyword.Constant),
      (
       '(class|interface|object|alias)(\\s+)',
       bygroups(Keyword.Declaration, Text), 'class'),
      (
       '(import)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "'\\\\.'|'[^\\\\]'|'\\\\\\{#[0-9a-fA-F]{4}\\}'", String.Char),
      (
       '".*``.*``.*"', String.Interpol),
      (
       '(\\.)([a-z_]\\w*)',
       bygroups(Operator, Name.Attribute)),
      (
       '[a-zA-Z_]\\w*:', Name.Label),
      (
       '[a-zA-Z_]\\w*', Name),
      (
       '[~^*!%&\\[\\](){}<>|+=:;,./?-]', Operator),
      (
       '\\d{1,3}(_\\d{3})+\\.\\d{1,3}(_\\d{3})+[kMGTPmunpf]?', Number.Float),
      (
       '\\d{1,3}(_\\d{3})+\\.[0-9]+([eE][+-]?[0-9]+)?[kMGTPmunpf]?',
       Number.Float),
      (
       '[0-9][0-9]*\\.\\d{1,3}(_\\d{3})+[kMGTPmunpf]?', Number.Float),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][+-]?[0-9]+)?[kMGTPmunpf]?',
       Number.Float),
      (
       '#([0-9a-fA-F]{4})(_[0-9a-fA-F]{4})+', Number.Hex),
      (
       '#[0-9a-fA-F]+', Number.Hex),
      (
       '\\$([01]{4})(_[01]{4})+', Number.Bin),
      (
       '\\$[01]+', Number.Bin),
      (
       '\\d{1,3}(_\\d{3})+[kMGTP]?', Number.Integer),
      (
       '[0-9]+[kMGTP]?', Number.Integer),
      (
       '\\n', Text)], 
     'class':[
      (
       '[A-Za-z_]\\w*', Name.Class, '#pop')], 
     'import':[
      (
       '[a-z][\\w.]*',
       Name.Namespace, '#pop')], 
     'comment':[
      (
       '[^*/]', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)]}


class KotlinLexer(RegexLexer):
    __doc__ = '\n    For `Kotlin <http://kotlinlang.org/>`_\n    source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'Kotlin'
    aliases = ['kotlin']
    filenames = ['*.kt']
    mimetypes = ['text/x-kotlin']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE
    kt_name = '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'
    kt_space_name = '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc', 'Zs') + ',-]*'
    kt_id = '(' + kt_name + '|`' + kt_space_name + '`)'
    tokens = {'root':[
      (
       '^\\s*\\[.*?\\]', Name.Attribute),
      (
       '[^\\S\\n]+', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/[*].*?[*]/', Comment.Multiline),
      (
       '""".*?"""', String),
      (
       '\\n', Text),
      (
       '::|!!|\\?[:.]', Operator),
      (
       '[~!%^&*()+=|\\[\\]:;,.<>/?-]', Punctuation),
      (
       '[{}]', Punctuation),
      (
       '@"(""|[^"])*"', String),
      (
       '"(\\\\\\\\|\\\\"|[^"\\n])*["\\n]', String),
      (
       "'\\\\.'|'[^\\\\]'", String.Char),
      (
       '[0-9](\\.[0-9]*)?([eE][+-][0-9]+)?[flFL]?|0[xX][0-9a-fA-F]+[Ll]?',
       Number),
      (
       '(object)(\\s+)(:)(\\s+)', bygroups(Keyword, Text, Punctuation, Text), 'class'),
      (
       '(companion)(\\s+)(object)', bygroups(Keyword, Text, Keyword)),
      (
       '(class|interface|object)(\\s+)', bygroups(Keyword, Text), 'class'),
      (
       '(package|import)(\\s+)', bygroups(Keyword, Text), 'package'),
      (
       '(val|var)(\\s+)([(])', bygroups(Keyword, Text, Punctuation), 'property_dec'),
      (
       '(val|var)(\\s+)', bygroups(Keyword, Text), 'property'),
      (
       '(fun)(\\s+)', bygroups(Keyword, Text), 'function'),
      (
       '(inline fun)(\\s+)', bygroups(Keyword, Text), 'function'),
      (
       '(abstract|annotation|as|break|by|catch|class|companion|const|constructor|continue|crossinline|data|do|dynamic|else|enum|external|false|final|finally|for|fun|get|if|import|in|infix|inline|inner|interface|internal|is|lateinit|noinline|null|object|open|operator|out|override|package|private|protected|public|reified|return|sealed|set|super|tailrec|this|throw|true|try|val|var|vararg|when|where|while)\\b',
       Keyword),
      (
       kt_id, Name)], 
     'package':[
      (
       '\\S+', Name.Namespace, '#pop')], 
     'class':[
      (
       kt_id, Name.Class, '#pop')], 
     'property':[
      (
       kt_id, Name.Property, '#pop')], 
     'property_dec':[
      (
       '(,)(\\s*)', bygroups(Punctuation, Text)),
      (
       '(:)(\\s*)', bygroups(Punctuation, Text)),
      (
       '<', Punctuation, 'generic'),
      (
       '([)])', Punctuation, '#pop'),
      (
       kt_id, Name.Property)], 
     'function':[
      (
       '<', Punctuation, 'generic'),
      (
       '' + kt_id + '([.])' + kt_id, bygroups(Name.Class, Punctuation, Name.Function), '#pop'),
      (
       kt_id, Name.Function, '#pop')], 
     'generic':[
      (
       '(>)(\\s*)', bygroups(Punctuation, Text), '#pop'),
      (
       ':', Punctuation),
      (
       '(reified|out|in)\\b', Keyword),
      (
       ',', Text),
      (
       '\\s+', Text),
      (
       kt_id, Name)]}


class XtendLexer(RegexLexer):
    __doc__ = '\n    For `Xtend <http://xtend-lang.org/>`_ source code.\n\n    .. versionadded:: 1.6\n    '
    name = 'Xtend'
    aliases = ['xtend']
    filenames = ['*.xtend']
    mimetypes = ['text/x-xtend']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root':[
      (
       '^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_$][\\w$]*)(\\s*)(\\()',
       bygroups(using(this), Name.Function, Text, Operator)),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '@[a-zA-Z_][\\w.]*', Name.Decorator),
      (
       '(assert|break|case|catch|continue|default|do|else|finally|for|if|goto|instanceof|new|return|switch|this|throw|try|while|IF|ELSE|ELSEIF|ENDIF|FOR|ENDFOR|SEPARATOR|BEFORE|AFTER)\\b',
       Keyword),
      (
       '(def|abstract|const|enum|extends|final|implements|native|private|protected|public|static|strictfp|super|synchronized|throws|transient|volatile)\\b',
       Keyword.Declaration),
      (
       '(boolean|byte|char|double|float|int|long|short|void)\\b',
       Keyword.Type),
      (
       '(package)(\\s+)', bygroups(Keyword.Namespace, Text)),
      (
       '(true|false|null)\\b', Keyword.Constant),
      (
       '(class|interface)(\\s+)', bygroups(Keyword.Declaration, Text),
       'class'),
      (
       '(import)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
      (
       "(''')", String, 'template'),
      (
       '(»)', String, 'template'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String),
      (
       '[a-zA-Z_]\\w*:', Name.Label),
      (
       '[a-zA-Z_$]\\w*', Name),
      (
       '[~^*!%&\\[\\](){}<>\\|+=:;,./?-]', Operator),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+L?', Number.Integer),
      (
       '\\n', Text)], 
     'class':[
      (
       '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     'import':[
      (
       '[\\w.]+\\*?', Name.Namespace, '#pop')], 
     'template':[
      (
       "'''", String, '#pop'),
      (
       '«', String, '#pop'),
      (
       '.', String)]}


class PigLexer(RegexLexer):
    __doc__ = '\n    For `Pig Latin <https://pig.apache.org/>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Pig'
    aliases = ['pig']
    filenames = ['*.pig']
    mimetypes = ['text/x-pig']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '--.*', Comment),
      (
       '/\\*[\\w\\W]*?\\*/', Comment.Multiline),
      (
       '\\\\\\n', Text),
      (
       '\\\\', Text),
      (
       "\\'(?:\\\\[ntbrf\\\\\\']|\\\\u[0-9a-f]{4}|[^\\'\\\\\\n\\r])*\\'", String),
      include('keywords'),
      include('types'),
      include('builtins'),
      include('punct'),
      include('operators'),
      (
       '[0-9]*\\.[0-9]+(e[0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-f]+', Number.Hex),
      (
       '[0-9]+L?', Number.Integer),
      (
       '\\n', Text),
      (
       '([a-z_]\\w*)(\\s*)(\\()',
       bygroups(Name.Function, Text, Punctuation)),
      (
       '[()#:]', Text),
      (
       '[^(:#\\\'")\\s]+', Text),
      (
       '\\S+\\s+', Text)], 
     'keywords':[
      (
       '(assert|and|any|all|arrange|as|asc|bag|by|cache|CASE|cat|cd|cp|%declare|%default|define|dense|desc|describe|distinct|du|dump|eval|exex|explain|filter|flatten|foreach|full|generate|group|help|if|illustrate|import|inner|input|into|is|join|kill|left|limit|load|ls|map|matches|mkdir|mv|not|null|onschema|or|order|outer|output|parallel|pig|pwd|quit|register|returns|right|rm|rmf|rollup|run|sample|set|ship|split|stderr|stdin|stdout|store|stream|through|union|using|void)\\b',
       Keyword)], 
     'builtins':[
      (
       '(AVG|BinStorage|cogroup|CONCAT|copyFromLocal|copyToLocal|COUNT|cross|DIFF|MAX|MIN|PigDump|PigStorage|SIZE|SUM|TextLoader|TOKENIZE)\\b',
       Name.Builtin)], 
     'types':[
      (
       '(bytearray|BIGINTEGER|BIGDECIMAL|chararray|datetime|double|float|int|long|tuple)\\b',
       Keyword.Type)], 
     'punct':[
      (
       '[;(){}\\[\\]]', Punctuation)], 
     'operators':[
      (
       '[#=,./%+\\-?]', Operator),
      (
       '(eq|gt|lt|gte|lte|neq|matches)\\b', Operator),
      (
       '(==|<=|<|>=|>|!=)', Operator)]}


class GoloLexer(RegexLexer):
    __doc__ = '\n    For `Golo <http://golo-lang.org/>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Golo'
    filenames = ['*.golo']
    aliases = ['golo']
    tokens = {'root':[
      (
       '[^\\S\\n]+', Text),
      (
       '#.*$', Comment),
      (
       '(\\^|\\.\\.\\.|:|\\?:|->|==|!=|=|\\+|\\*|%|/|<=|<|>=|>|=|\\.)',
       Operator),
      (
       '(?<=[^-])(-)(?=[^-])', Operator),
      (
       '(?<=[^`])(is|isnt|and|or|not|oftype|in|orIfNull)\\b', Operator.Word),
      (
       '[]{}|(),[]', Punctuation),
      (
       '(module|import)(\\s+)',
       bygroups(Keyword.Namespace, Text),
       'modname'),
      (
       '\\b([a-zA-Z_][\\w$.]*)(::)', bygroups(Name.Namespace, Punctuation)),
      (
       '\\b([a-zA-Z_][\\w$]*(?:\\.[a-zA-Z_][\\w$]*)+)\\b', Name.Namespace),
      (
       '(let|var)(\\s+)',
       bygroups(Keyword.Declaration, Text),
       'varname'),
      (
       '(struct)(\\s+)',
       bygroups(Keyword.Declaration, Text),
       'structname'),
      (
       '(function)(\\s+)',
       bygroups(Keyword.Declaration, Text),
       'funcname'),
      (
       '(null|true|false)\\b', Keyword.Constant),
      (
       '(augment|pimp|if|else|case|match|return|case|when|then|otherwise|while|for|foreach|try|catch|finally|throw|local|continue|break)\\b',
       Keyword),
      (
       '(map|array|list|set|vector|tuple)(\\[)',
       bygroups(Name.Builtin, Punctuation)),
      (
       '(print|println|readln|raise|fun|asInterfaceInstance)\\b',
       Name.Builtin),
      (
       '(`?[a-zA-Z_][\\w$]*)(\\()',
       bygroups(Name.Function, Punctuation)),
      (
       '-?[\\d_]*\\.[\\d_]*([eE][+-]?\\d[\\d_]*)?F?', Number.Float),
      (
       '0[0-7]+j?', Number.Oct),
      (
       '0[xX][a-fA-F0-9]+', Number.Hex),
      (
       '-?\\d[\\d_]*L', Number.Integer.Long),
      (
       '-?\\d[\\d_]*', Number.Integer),
      (
       '`?[a-zA-Z_][\\w$]*', Name),
      (
       '@[a-zA-Z_][\\w$.]*', Name.Decorator),
      (
       '"""', String, combined('stringescape', 'triplestring')),
      (
       '"', String, combined('stringescape', 'doublestring')),
      (
       "'", String, combined('stringescape', 'singlestring')),
      (
       '----((.|\\n)*?)----', String.Doc)], 
     'funcname':[
      (
       '`?[a-zA-Z_][\\w$]*', Name.Function, '#pop')], 
     'modname':[
      (
       '[a-zA-Z_][\\w$.]*\\*?', Name.Namespace, '#pop')], 
     'structname':[
      (
       '`?[\\w.]+\\*?', Name.Class, '#pop')], 
     'varname':[
      (
       '`?[a-zA-Z_][\\w$]*', Name.Variable, '#pop')], 
     'string':[
      (
       '[^\\\\\\\'"\\n]+', String),
      (
       '[\\\'"\\\\]', String)], 
     'stringescape':[
      (
       '\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
       String.Escape)], 
     'triplestring':[
      (
       '"""', String, '#pop'),
      include('string'),
      (
       '\\n', String)], 
     'doublestring':[
      (
       '"', String.Double, '#pop'),
      include('string')], 
     'singlestring':[
      (
       "'", String, '#pop'),
      include('string')], 
     'operators':[
      (
       '[#=,./%+\\-?]', Operator),
      (
       '(eq|gt|lt|gte|lte|neq|matches)\\b', Operator),
      (
       '(==|<=|<|>=|>|!=)', Operator)]}


class JasminLexer(RegexLexer):
    __doc__ = '\n    For `Jasmin <http://jasmin.sourceforge.net/>`_ assembly code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Jasmin'
    aliases = ['jasmin', 'jasminxt']
    filenames = ['*.j']
    _whitespace = ' \\n\\t\\r'
    _ws = '(?:[%s]+)' % _whitespace
    _separator = '%s:=' % _whitespace
    _break = '(?=[%s]|$)' % _separator
    _name = '[^%s]+' % _separator
    _unqualified_name = '(?:[^%s.;\\[/]+)' % _separator
    tokens = {'default':[
      (
       '\\n', Text, '#pop'),
      (
       "'", String.Single, ('#pop', 'quote')),
      (
       '"', String.Double, 'string'),
      (
       '=', Punctuation),
      (
       ':', Punctuation, 'label'),
      (
       _ws, Text),
      (
       ';.*', Comment.Single),
      (
       '(\\$[-+])?0x-?[\\da-fA-F]+%s' % _break, Number.Hex),
      (
       '(\\$[-+]|\\+)?-?\\d+%s' % _break, Number.Integer),
      (
       '-?(\\d+\\.\\d*|\\.\\d+)([eE][-+]?\\d+)?[fFdD]?[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]*%s' % _break, Number.Float),
      (
       '\\$%s' % _name, Name.Variable),
      (
       '\\.annotation%s' % _break, Keyword.Reserved, 'annotation'),
      (
       '(\\.attribute|\\.bytecode|\\.debug|\\.deprecated|\\.enclosing|\\.interface|\\.line|\\.signature|\\.source|\\.stack|\\.var|abstract|annotation|bridge|class|default|enum|field|final|fpstrict|interface|native|private|protected|public|signature|static|synchronized|synthetic|transient|varargs|volatile)%s' % _break,
       Keyword.Reserved),
      (
       '\\.catch%s' % _break, Keyword.Reserved, 'caught-exception'),
      (
       '(\\.class|\\.implements|\\.inner|\\.super|inner|invisible|invisibleparam|outer|visible|visibleparam)%s' % _break,
       Keyword.Reserved, 'class/convert-dots'),
      (
       '\\.field%s' % _break, Keyword.Reserved,
       ('descriptor/convert-dots', 'field')),
      (
       '(\\.end|\\.limit|use)%s' % _break, Keyword.Reserved,
       'no-verification'),
      (
       '\\.method%s' % _break, Keyword.Reserved, 'method'),
      (
       '\\.set%s' % _break, Keyword.Reserved, 'var'),
      (
       '\\.throws%s' % _break, Keyword.Reserved, 'exception'),
      (
       '(from|offset|to|using)%s' % _break, Keyword.Reserved, 'label'),
      (
       'is%s' % _break, Keyword.Reserved,
       ('descriptor/convert-dots', 'var')),
      (
       '(locals|stack)%s' % _break, Keyword.Reserved, 'verification'),
      (
       'method%s' % _break, Keyword.Reserved, 'enclosing-method'),
      (
       words(('aaload', 'aastore', 'aconst_null', 'aload', 'aload_0', 'aload_1', 'aload_2',
       'aload_3', 'aload_w', 'areturn', 'arraylength', 'astore', 'astore_0', 'astore_1',
       'astore_2', 'astore_3', 'astore_w', 'athrow', 'baload', 'bastore', 'bipush',
       'breakpoint', 'caload', 'castore', 'd2f', 'd2i', 'd2l', 'dadd', 'daload',
       'dastore', 'dcmpg', 'dcmpl', 'dconst_0', 'dconst_1', 'ddiv', 'dload', 'dload_0',
       'dload_1', 'dload_2', 'dload_3', 'dload_w', 'dmul', 'dneg', 'drem', 'dreturn',
       'dstore', 'dstore_0', 'dstore_1', 'dstore_2', 'dstore_3', 'dstore_w', 'dsub',
       'dup', 'dup2', 'dup2_x1', 'dup2_x2', 'dup_x1', 'dup_x2', 'f2d', 'f2i', 'f2l',
       'fadd', 'faload', 'fastore', 'fcmpg', 'fcmpl', 'fconst_0', 'fconst_1', 'fconst_2',
       'fdiv', 'fload', 'fload_0', 'fload_1', 'fload_2', 'fload_3', 'fload_w', 'fmul',
       'fneg', 'frem', 'freturn', 'fstore', 'fstore_0', 'fstore_1', 'fstore_2', 'fstore_3',
       'fstore_w', 'fsub', 'i2b', 'i2c', 'i2d', 'i2f', 'i2l', 'i2s', 'iadd', 'iaload',
       'iand', 'iastore', 'iconst_0', 'iconst_1', 'iconst_2', 'iconst_3', 'iconst_4',
       'iconst_5', 'iconst_m1', 'idiv', 'iinc', 'iinc_w', 'iload', 'iload_0', 'iload_1',
       'iload_2', 'iload_3', 'iload_w', 'imul', 'ineg', 'int2byte', 'int2char', 'int2short',
       'ior', 'irem', 'ireturn', 'ishl', 'ishr', 'istore', 'istore_0', 'istore_1',
       'istore_2', 'istore_3', 'istore_w', 'isub', 'iushr', 'ixor', 'l2d', 'l2f',
       'l2i', 'ladd', 'laload', 'land', 'lastore', 'lcmp', 'lconst_0', 'lconst_1',
       'ldc2_w', 'ldiv', 'lload', 'lload_0', 'lload_1', 'lload_2', 'lload_3', 'lload_w',
       'lmul', 'lneg', 'lookupswitch', 'lor', 'lrem', 'lreturn', 'lshl', 'lshr',
       'lstore', 'lstore_0', 'lstore_1', 'lstore_2', 'lstore_3', 'lstore_w', 'lsub',
       'lushr', 'lxor', 'monitorenter', 'monitorexit', 'nop', 'pop', 'pop2', 'ret',
       'ret_w', 'return', 'saload', 'sastore', 'sipush', 'swap'),
         suffix=_break), Keyword.Reserved),
      (
       '(anewarray|checkcast|instanceof|ldc|ldc_w|new)%s' % _break,
       Keyword.Reserved, 'class/no-dots'),
      (
       'invoke(dynamic|interface|nonvirtual|special|static|virtual)%s' % _break, Keyword.Reserved,
       'invocation'),
      (
       '(getfield|putfield)%s' % _break, Keyword.Reserved,
       ('descriptor/no-dots', 'field')),
      (
       '(getstatic|putstatic)%s' % _break, Keyword.Reserved,
       ('descriptor/no-dots', 'static')),
      (
       words(('goto', 'goto_w', 'if_acmpeq', 'if_acmpne', 'if_icmpeq', 'if_icmpge', 'if_icmpgt',
       'if_icmple', 'if_icmplt', 'if_icmpne', 'ifeq', 'ifge', 'ifgt', 'ifle', 'iflt',
       'ifne', 'ifnonnull', 'ifnull', 'jsr', 'jsr_w'),
         suffix=_break),
       Keyword.Reserved, 'label'),
      (
       '(multianewarray|newarray)%s' % _break, Keyword.Reserved,
       'descriptor/convert-dots'),
      (
       'tableswitch%s' % _break, Keyword.Reserved, 'table')], 
     'quote':[
      (
       "'", String.Single, '#pop'),
      (
       '\\\\u[\\da-fA-F]{4}', String.Escape),
      (
       "[^'\\\\]+", String.Single)], 
     'string':[
      (
       '"', String.Double, '#pop'),
      (
       '\\\\([nrtfb"\\\'\\\\]|u[\\da-fA-F]{4}|[0-3]?[0-7]{1,2})',
       String.Escape),
      (
       '[^"\\\\]+', String.Double)], 
     'root':[
      (
       '\\n+', Text),
      (
       "'", String.Single, 'quote'),
      include('default'),
      (
       '(%s)([ \\t\\r]*)(:)' % _name,
       bygroups(Name.Label, Text, Punctuation)),
      (
       _name, String.Other)], 
     'annotation':[
      (
       '\\n', Text, ('#pop', 'annotation-body')),
      (
       'default%s' % _break, Keyword.Reserved,
       ('#pop', 'annotation-default')),
      include('default')], 
     'annotation-body':[
      (
       '\\n+', Text),
      (
       '\\.end%s' % _break, Keyword.Reserved, '#pop'),
      include('default'),
      (
       _name, String.Other, ('annotation-items', 'descriptor/no-dots'))], 
     'annotation-default':[
      (
       '\\n+', Text),
      (
       '\\.end%s' % _break, Keyword.Reserved, '#pop'),
      include('default'),
      default(('annotation-items', 'descriptor/no-dots'))], 
     'annotation-items':[
      (
       "'", String.Single, 'quote'),
      include('default'),
      (
       _name, String.Other)], 
     'caught-exception':[
      (
       'all%s' % _break, Keyword, '#pop'),
      include('exception')], 
     'class/convert-dots':[
      include('default'),
      (
       '(L)((?:%s[/.])*)(%s)(;)' % (_unqualified_name, _name),
       bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
       '#pop'),
      (
       '((?:%s[/.])*)(%s)' % (_unqualified_name, _name),
       bygroups(Name.Namespace, Name.Class), '#pop')], 
     'class/no-dots':[
      include('default'),
      (
       '\\[+', Punctuation, ('#pop', 'descriptor/no-dots')),
      (
       '(L)((?:%s/)*)(%s)(;)' % (_unqualified_name, _name),
       bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
       '#pop'),
      (
       '((?:%s/)*)(%s)' % (_unqualified_name, _name),
       bygroups(Name.Namespace, Name.Class), '#pop')], 
     'descriptor/convert-dots':[
      include('default'),
      (
       '\\[+', Punctuation),
      (
       '(L)((?:%s[/.])*)(%s?)(;)' % (_unqualified_name, _name),
       bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
       '#pop'),
      (
       '[^%s\\[)L]+' % _separator, Keyword.Type, '#pop'),
      default('#pop')], 
     'descriptor/no-dots':[
      include('default'),
      (
       '\\[+', Punctuation),
      (
       '(L)((?:%s/)*)(%s)(;)' % (_unqualified_name, _name),
       bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
       '#pop'),
      (
       '[^%s\\[)L]+' % _separator, Keyword.Type, '#pop'),
      default('#pop')], 
     'descriptors/convert-dots':[
      (
       '\\)', Punctuation, '#pop'),
      default('descriptor/convert-dots')], 
     'enclosing-method':[
      (
       _ws, Text),
      (
       '(?=[^%s]*\\()' % _separator, Text, ('#pop', 'invocation')),
      default(('#pop', 'class/convert-dots'))], 
     'exception':[
      include('default'),
      (
       '((?:%s[/.])*)(%s)' % (_unqualified_name, _name),
       bygroups(Name.Namespace, Name.Exception), '#pop')], 
     'field':[
      (
       'static%s' % _break, Keyword.Reserved, ('#pop', 'static')),
      include('default'),
      (
       '((?:%s[/.](?=[^%s]*[/.]))*)(%s[/.])?(%s)' % (
        _unqualified_name, _separator, _unqualified_name, _name),
       bygroups(Name.Namespace, Name.Class, Name.Variable.Instance),
       '#pop')], 
     'invocation':[
      include('default'),
      (
       '((?:%s[/.](?=[^%s(]*[/.]))*)(%s[/.])?(%s)(\\()' % (
        _unqualified_name, _separator, _unqualified_name, _name),
       bygroups(Name.Namespace, Name.Class, Name.Function, Punctuation),
       ('#pop', 'descriptor/convert-dots', 'descriptors/convert-dots', 'descriptor/convert-dots'))], 
     'label':[
      include('default'),
      (
       _name, Name.Label, '#pop')], 
     'method':[
      include('default'),
      (
       '(%s)(\\()' % _name, bygroups(Name.Function, Punctuation),
       ('#pop', 'descriptor/convert-dots', 'descriptors/convert-dots', 'descriptor/convert-dots'))], 
     'no-verification':[
      (
       '(locals|method|stack)%s' % _break, Keyword.Reserved, '#pop'),
      include('default')], 
     'static':[
      include('default'),
      (
       '((?:%s[/.](?=[^%s]*[/.]))*)(%s[/.])?(%s)' % (
        _unqualified_name, _separator, _unqualified_name, _name),
       bygroups(Name.Namespace, Name.Class, Name.Variable.Class), '#pop')], 
     'table':[
      (
       '\\n+', Text),
      (
       'default%s' % _break, Keyword.Reserved, '#pop'),
      include('default'),
      (
       _name, Name.Label)], 
     'var':[
      include('default'),
      (
       _name, Name.Variable, '#pop')], 
     'verification':[
      include('default'),
      (
       '(Double|Float|Integer|Long|Null|Top|UninitializedThis)%s' % _break, Keyword, '#pop'),
      (
       'Object%s' % _break, Keyword, ('#pop', 'class/no-dots')),
      (
       'Uninitialized%s' % _break, Keyword, ('#pop', 'label'))]}

    def analyse_text(text):
        score = 0
        if re.search('^\\s*\\.class\\s', text, re.MULTILINE):
            score += 0.5
            if re.search('^\\s*[a-z]+_[a-z]+\\b', text, re.MULTILINE):
                score += 0.3
        if re.search('^\\s*\\.(attribute|bytecode|debug|deprecated|enclosing|inner|interface|limit|set|signature|stack)\\b', text, re.MULTILINE):
            score += 0.6
        return score


class SarlLexer(RegexLexer):
    __doc__ = '\n\tFor `SARL <http://www.sarl.io>`_ source code.\n\t\n\t.. versionadded:: 2.4\n\t'
    name = 'SARL'
    aliases = ['sarl']
    filenames = ['*.sarl']
    mimetypes = ['text/x-sarl']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root':[
      (
       '^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_$][\\w$]*)(\\s*)(\\()',
       bygroups(using(this), Name.Function, Text, Operator)),
      (
       '[^\\S\\n]+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '@[a-zA-Z_][\\w.]*', Name.Decorator),
      (
       '(as|break|case|catch|default|do|else|extends|extension|finally|fires|for|if|implements|instanceof|new|on|requires|return|super|switch|throw|throws|try|typeof|uses|while|with)\\b',
       Keyword),
      (
       '(abstract|def|dispatch|final|native|override|private|protected|public|static|strictfp|synchronized|transient|val|var|volatile)\\b', Keyword.Declaration),
      (
       '(boolean|byte|char|double|float|int|long|short|void)\\b',
       Keyword.Type),
      (
       '(package)(\\s+)', bygroups(Keyword.Namespace, Text)),
      (
       '(false|it|null|occurrence|this|true|void)\\b', Keyword.Constant),
      (
       '(agent|annotation|artifact|behavior|capacity|class|enum|event|interface|skill|space)(\\s+)', bygroups(Keyword.Declaration, Text),
       'class'),
      (
       '(import)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String),
      (
       '[a-zA-Z_]\\w*:', Name.Label),
      (
       '[a-zA-Z_$]\\w*', Name),
      (
       '[~^*!%&\\[\\](){}<>\\|+=:;,./?-]', Operator),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+L?', Number.Integer),
      (
       '\\n', Text)], 
     'class':[
      (
       '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     'import':[
      (
       '[\\w.]+\\*?', Name.Namespace, '#pop')]}