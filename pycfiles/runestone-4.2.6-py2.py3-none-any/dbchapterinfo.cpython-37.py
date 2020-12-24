# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/chapterdb/dbchapterinfo.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 7611 bytes
__author__ = 'bmiller'
import re, datetime, os.path
from collections import OrderedDict
import docutils
from sqlalchemy import Table, select, and_, or_
from runestone.server.componentdb import engine, meta, sess
from sphinx.util import logging
logger = logging.getLogger(__name__)
ignored_chapters = [
 '', 'FrontBackMatter', 'Appendices']

def setup(app):
    """
    The setup function ensures that we install this module as a Sphinx extension. Even though
    we are not going for a new directive or role we can use the extension mechanism to add
    specific event handlers.
    """
    app.connect('env-updated', env_updated)


def update_database(chaptitles, subtitles, skips, app):
    """
    When the build is completely finished output the information gathered about
    chapters and subchapters into the database.
    """
    if not sess:
        logger.info('You need to install a DBAPI module - psycopg2 for Postgres')
        logger.info('Or perhaps you have not set your DBURL environment variable')
        return
    else:
        chapters = Table('chapters', meta, autoload=True, autoload_with=engine)
        sub_chapters = Table('sub_chapters', meta, autoload=True, autoload_with=engine)
        questions = Table('questions', meta, autoload=True, autoload_with=engine)
        basecourse = app.config.html_context.get('basecourse', 'unknown')
        dynamic_pages = app.config.html_context.get('dynamic_pages', False)
        if dynamic_pages:
            cname = basecourse
        else:
            cname = app.env.config.html_context.get('course_id', 'unknown')
    logger.info('Cleaning up old chapters info for {}'.format(cname))
    sess.execute(chapters.delete().where(chapters.c.course_id == basecourse))
    logger.info('Populating the database with Chapter information')
    chapnum = 1
    for chapnum, chap in enumerate(chaptitles, start=1):
        logger.info('Adding chapter subchapter info for {}'.format(chap))
        ins = chapters.insert().values(chapter_name=(chaptitles.get(chap, chap)),
          course_id=cname,
          chapter_label=chap,
          chapter_num=chapnum)
        res = sess.execute(ins)
        currentRowId = res.inserted_primary_key[0]
        for subchapnum, sub in enumerate((subtitles[chap]), start=1):
            if (
             chap, sub) in skips:
                skipreading = 'T'
            else:
                skipreading = 'F'
            q_name = '{}/{}'.format(chaptitles.get(chap, chap), subtitles[chap][sub])
            ins = sub_chapters.insert().values(sub_chapter_name=(subtitles[chap][sub]),
              chapter_id=(str(currentRowId)),
              sub_chapter_label=sub,
              skipreading=skipreading,
              sub_chapter_num=subchapnum)
            sess.execute(ins)
            sel = select([questions]).where(or_(and_(questions.c.chapter == chap, questions.c.subchapter == sub, questions.c.question_type == 'page', questions.c.base_course == basecourse), and_(questions.c.name == q_name, questions.c.question_type == 'page', questions.c.base_course == basecourse)))
            res = sess.execute(sel).first()
            if res:
                if res.name != q_name or res.chapter != chap or res.subchapter != sub:
                    upd = questions.update().where(questions.c.id == res['id']).values(name=q_name,
                      chapter=chap,
                      from_source='T',
                      subchapter=sub)
                    sess.execute(upd)
                ins = res or questions.insert().values(chapter=chap,
                  subchapter=sub,
                  question_type='page',
                  from_source='T',
                  name=q_name,
                  timestamp=(datetime.datetime.now()),
                  base_course=basecourse)
                sess.execute(ins)


def env_updated(app, env):
    """
    This may be the best place to walk the completed document with TOC
    """
    relations = env.collect_relations()
    included_docs = []
    updated_docs = []
    cur_doc = env.config.master_doc
    while cur_doc:
        included_docs.append(cur_doc)
        doctree = env.get_doctree(cur_doc)
        cur_doc = relations[cur_doc][2]

    chap_titles = OrderedDict()
    subchap_titles = OrderedDict()
    skips = OrderedDict()
    for docname in included_docs:
        doctree = env.get_doctree(docname)
        for section in doctree.traverse(docutils.nodes.section):
            updated_docs.append(docname)
            title = section.next_node(docutils.nodes.Titular)
            splits = docname.split('/')
            chap_id = splits[(-2)] if len(splits) > 1 else ''
            subchap_id = splits[(-1)]
            if hasattr(env, 'skipreading'):
                if docname in env.skipreading:
                    skips[(chap_id, subchap_id)] = True
                else:
                    if chap_id in ignored_chapters or subchap_id == 'index':
                        continue
                    if chap_id not in chap_titles:
                        if subchap_id == 'toctree':
                            chap_titles[chap_id] = title.astext()
                        else:
                            chap_titles[chap_id] = chap_id
                            logger.warning(docname + ' Using a substandard chapter title')
                if chap_id not in subchap_titles:
                    subchap_titles[chap_id] = OrderedDict()
                if subchap_id not in subchap_titles[chap_id] and subchap_id != 'toctree':
                    subchap_titles[chap_id][subchap_id] = title.astext()

    update_database(chap_titles, subchap_titles, skips, app)
    return []