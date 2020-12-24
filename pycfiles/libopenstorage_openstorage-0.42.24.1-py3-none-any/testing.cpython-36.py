# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/testing.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 10752 bytes
"""
    pygments.lexers.testing
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for testing languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Comment, Keyword, Name, String, Number, Generic, Text
__all__ = [
 'GherkinLexer', 'TAPLexer']

class GherkinLexer(RegexLexer):
    __doc__ = '\n    For `Gherkin <http://github.com/aslakhellesoy/gherkin/>` syntax.\n\n    .. versionadded:: 1.2\n    '
    name = 'Gherkin'
    aliases = ['cucumber', 'gherkin']
    filenames = ['*.feature']
    mimetypes = ['text/x-gherkin']
    feature_keywords = '^(기능|機能|功能|フィーチャ|خاصية|תכונה|Функціонал|Функционалност|Функционал|Фича|Особина|Могућност|Özellik|Właściwość|Tính năng|Trajto|Savybė|Požiadavka|Požadavek|Osobina|Ominaisuus|Omadus|OH HAI|Mogućnost|Mogucnost|Jellemző|Fīča|Funzionalità|Funktionalität|Funkcionalnost|Funkcionalitāte|Funcționalitate|Functionaliteit|Functionalitate|Funcionalitat|Funcionalidade|Fonctionnalité|Fitur|Feature|Egenskap|Egenskab|Crikey|Característica|Arwedd)(:)(.*)$'
    feature_element_keywords = "^(\\s*)(시나리오 개요|시나리오|배경|背景|場景大綱|場景|场景大纲|场景|劇本大綱|劇本|剧本大纲|剧本|テンプレ|シナリオテンプレート|シナリオテンプレ|シナリオアウトライン|シナリオ|سيناريو مخطط|سيناريو|الخلفية|תרחיש|תבנית תרחיש|רקע|Тарих|Сценарій|Сценарио|Сценарий структураси|Сценарий|Структура сценарію|Структура сценарија|Структура сценария|Скица|Рамка на сценарий|Пример|Предыстория|Предистория|Позадина|Передумова|Основа|Концепт|Контекст|Założenia|Wharrimean is|Tình huống|The thing of it is|Tausta|Taust|Tapausaihio|Tapaus|Szenariogrundriss|Szenario|Szablon scenariusza|Stsenaarium|Struktura scenarija|Skica|Skenario konsep|Skenario|Situācija|Senaryo taslağı|Senaryo|Scénář|Scénario|Schema dello scenario|Scenārijs pēc parauga|Scenārijs|Scenár|Scenaro|Scenariusz|Scenariul de şablon|Scenariul de sablon|Scenariu|Scenario Outline|Scenario Amlinellol|Scenario|Scenarijus|Scenarijaus šablonas|Scenarij|Scenarie|Rerefons|Raamstsenaarium|Primer|Pozadí|Pozadina|Pozadie|Plan du scénario|Plan du Scénario|Osnova scénáře|Osnova|Náčrt Scénáře|Náčrt Scenáru|Mate|MISHUN SRSLY|MISHUN|Kịch bản|Konturo de la scenaro|Kontext|Konteksts|Kontekstas|Kontekst|Koncept|Khung tình huống|Khung kịch bản|Háttér|Grundlage|Geçmiş|Forgatókönyv vázlat|Forgatókönyv|Fono|Esquema do Cenário|Esquema do Cenario|Esquema del escenario|Esquema de l'escenari|Escenario|Escenari|Dis is what went down|Dasar|Contexto|Contexte|Contesto|Condiţii|Conditii|Cenário|Cenario|Cefndir|Bối cảnh|Blokes|Bakgrunn|Bakgrund|Baggrund|Background|B4|Antecedents|Antecedentes|All y'all|Achtergrond|Abstrakt Scenario|Abstract Scenario)(:)(.*)$"
    examples_keywords = '^(\\s*)(예|例子|例|サンプル|امثلة|דוגמאות|Сценарији|Примери|Приклади|Мисоллар|Значения|Örnekler|Voorbeelden|Variantai|Tapaukset|Scenarios|Scenariji|Scenarijai|Příklady|Példák|Príklady|Przykłady|Primjeri|Primeri|Piemēri|Pavyzdžiai|Paraugs|Juhtumid|Exemplos|Exemples|Exemplele|Exempel|Examples|Esempi|Enghreifftiau|Ekzemploj|Eksempler|Ejemplos|EXAMPLZ|Dữ liệu|Contoh|Cobber|Beispiele)(:)(.*)$'
    step_keywords = "^(\\s*)(하지만|조건|먼저|만일|만약|단|그리고|그러면|那麼|那么|而且|當|当|前提|假設|假设|假如|假定|但是|但し|並且|并且|同時|同时|もし|ならば|ただし|しかし|かつ|و |متى |لكن |عندما |ثم |بفرض |اذاً |כאשר |וגם |בהינתן |אזי |אז |אבל |Якщо |Унда |То |Припустимо, що |Припустимо |Онда |Но |Нехай |Лекин |Когато |Када |Кад |К тому же |И |Задато |Задати |Задате |Если |Допустим |Дадено |Ва |Бирок |Аммо |Али |Але |Агар |А |І |Și |És |Zatati |Zakładając |Zadato |Zadate |Zadano |Zadani |Zadan |Youse know when youse got |Youse know like when |Yna |Ya know how |Ya gotta |Y |Wun |Wtedy |When y'all |When |Wenn |WEN |Và |Ve |Und |Un |Thì |Then y'all |Then |Tapi |Tak |Tada |Tad |Så |Stel |Soit |Siis |Si |Sed |Se |Quando |Quand |Quan |Pryd |Pokud |Pokiaľ |Però |Pero |Pak |Oraz |Onda |Ond |Oletetaan |Og |Och |O zaman |Når |När |Niin |Nhưng |N |Mutta |Men |Mas |Maka |Majd |Mais |Maar |Ma |Lorsque |Lorsqu'|Kun |Kuid |Kui |Khi |Keď |Ketika |Když |Kaj |Kai |Kada |Kad |Jeżeli |Ja |Ir |I CAN HAZ |I |Ha |Givun |Givet |Given y'all |Given |Gitt |Gegeven |Gegeben sei |Fakat |Eğer ki |Etant donné |Et |Então |Entonces |Entao |En |Eeldades |E |Duota |Dun |Donitaĵo |Donat |Donada |Do |Diyelim ki |Dengan |Den youse gotta |De |Dato |Dar |Dann |Dan |Dado |Dacă |Daca |DEN |Când |Cuando |Cho |Cept |Cand |Cal |But y'all |But |Buh |Biết |Bet |BUT |Atès |Atunci |Atesa |Anrhegedig a |Angenommen |And y'all |And |An |Ama |Als |Alors |Allora |Ali |Aleshores |Ale |Akkor |Aber |AN |A také |A |\\* )"
    tokens = {'comments':[
      (
       '^\\s*#.*$', Comment)], 
     'feature_elements':[
      (
       step_keywords, Keyword, 'step_content_stack'),
      include('comments'),
      (
       '(\\s|.)', Name.Function)], 
     'feature_elements_on_stack':[
      (
       step_keywords, Keyword, '#pop:2'),
      include('comments'),
      (
       '(\\s|.)', Name.Function)], 
     'examples_table':[
      (
       '\\s+\\|', Keyword, 'examples_table_header'),
      include('comments'),
      (
       '(\\s|.)', Name.Function)], 
     'examples_table_header':[
      (
       '\\s+\\|\\s*$', Keyword, '#pop:2'),
      include('comments'),
      (
       '\\\\\\|', Name.Variable),
      (
       '\\s*\\|', Keyword),
      (
       '[^|]', Name.Variable)], 
     'scenario_sections_on_stack':[
      (
       feature_element_keywords,
       bygroups(Name.Function, Keyword, Keyword, Name.Function),
       'feature_elements_on_stack')], 
     'narrative':[
      include('scenario_sections_on_stack'),
      include('comments'),
      (
       '(\\s|.)', Name.Function)], 
     'table_vars':[
      (
       '(<[^>]+>)', Name.Variable)], 
     'numbers':[
      (
       '(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', String)], 
     'string':[
      include('table_vars'),
      (
       '(\\s|.)', String)], 
     'py_string':[
      (
       '"""', Keyword, '#pop'),
      include('string')], 
     'step_content_root':[
      (
       '$', Keyword, '#pop'),
      include('step_content')], 
     'step_content_stack':[
      (
       '$', Keyword, '#pop:2'),
      include('step_content')], 
     'step_content':[
      (
       '"', Name.Function, 'double_string'),
      include('table_vars'),
      include('numbers'),
      include('comments'),
      (
       '(\\s|.)', Name.Function)], 
     'table_content':[
      (
       '\\s+\\|\\s*$', Keyword, '#pop'),
      include('comments'),
      (
       '\\\\\\|', String),
      (
       '\\s*\\|', Keyword),
      include('string')], 
     'double_string':[
      (
       '"', Name.Function, '#pop'),
      include('string')], 
     'root':[
      (
       '\\n', Name.Function),
      include('comments'),
      (
       '"""', Keyword, 'py_string'),
      (
       '\\s+\\|', Keyword, 'table_content'),
      (
       '"', Name.Function, 'double_string'),
      include('table_vars'),
      include('numbers'),
      (
       '(\\s*)(@[^@\\r\\n\\t ]+)', bygroups(Name.Function, Name.Tag)),
      (
       step_keywords, bygroups(Name.Function, Keyword),
       'step_content_root'),
      (
       feature_keywords, bygroups(Keyword, Keyword, Name.Function),
       'narrative'),
      (
       feature_element_keywords,
       bygroups(Name.Function, Keyword, Keyword, Name.Function),
       'feature_elements'),
      (
       examples_keywords,
       bygroups(Name.Function, Keyword, Keyword, Name.Function),
       'examples_table'),
      (
       '(\\s|.)', Name.Function)]}


class TAPLexer(RegexLexer):
    __doc__ = '\n    For Test Anything Protocol (TAP) output.\n\n    .. versionadded:: 2.1\n    '
    name = 'TAP'
    aliases = ['tap']
    filenames = ['*.tap']
    tokens = {'root':[
      (
       '^TAP version \\d+\\n', Name.Namespace),
      (
       '^1\\.\\.\\d+', Keyword.Declaration, 'plan'),
      (
       '^(not ok)([^\\S\\n]*)(\\d*)',
       bygroups(Generic.Error, Text, Number.Integer), 'test'),
      (
       '^(ok)([^\\S\\n]*)(\\d*)',
       bygroups(Keyword.Reserved, Text, Number.Integer), 'test'),
      (
       '^#.*\\n', Comment),
      (
       '^Bail out!.*\\n', Generic.Error),
      (
       '^.*\\n', Text)], 
     'plan':[
      (
       '[^\\S\\n]+', Text),
      (
       '#', Comment, 'directive'),
      (
       '\\n', Comment, '#pop'),
      (
       '.*\\n', Generic.Error, '#pop')], 
     'test':[
      (
       '[^\\S\\n]+', Text),
      (
       '#', Comment, 'directive'),
      (
       '\\S+', Text),
      (
       '\\n', Text, '#pop')], 
     'directive':[
      (
       '[^\\S\\n]+', Comment),
      (
       '(?i)\\bTODO\\b', Comment.Preproc),
      (
       '(?i)\\bSKIP\\S*', Comment.Preproc),
      (
       '\\S+', Comment),
      (
       '\\n', Comment, '#pop:2')]}