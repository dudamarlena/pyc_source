# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neptuno/default/update/update.py
# Compiled at: 2012-10-29 11:33:17
import os, sys, re, subprocess as sp
from config import CONFIG
sys.path = sys.path + CONFIG['paths']
from nucleo.config import CONFIGURACION
current_path = os.path.dirname(os.path.abspath(__file__))

def actualizar(modo='post'):
    if modo.lower() not in ('pre', 'post'):
        raise Exception('Modo "%s" incorrecto' % modo)
    sys.stdout.write('Actualizando en modo [%s]\n' % modo)
    DONE = os.path.join(current_path, 'DONE')
    TODO = os.path.join(current_path, 'TODO')
    realizados = []
    if os.path.exists(DONE):
        f_done = file(DONE, 'rb')
        try:
            for linea in f_done:
                m_issue = re.search('^([\\w./-]+)\\s+(pre|post)', linea)
                if m_issue:
                    current_issue = '%s %s' % (m_issue.group(1),
                     m_issue.group(2))
                    if m_issue.group(2) == modo.lower() and current_issue not in realizados:
                        realizados.append('%s %s' % (m_issue.group(1),
                         m_issue.group(2)))

        finally:
            f_done.close()

    f_todo = file(TODO, 'rb')
    f_done = file(DONE, 'a')
    try:
        for linea in f_todo:
            m_coment = re.search('^#.+', linea)
            if m_coment:
                continue
            m_issue = re.search('^([\\w\\-\\._]+)\\s+(pre|post)\\s+([\\w./-]+)', linea, re.I | re.U)
            if m_issue:
                current_issue = '%s %s' % (m_issue.group(1),
                 m_issue.group(2))
                if current_issue in realizados or m_issue.group(2).lower() != modo.lower():
                    sys.stderr.write('Saltando actualización [%s] \n' % current_issue)
                else:
                    sys.stdout.write('Actualizando [%s]\n' % current_issue)
                    ext = os.path.splitext(m_issue.group(3))[1]
                    try:
                        if ext == '.py':
                            sys.stdout.write('Ejecutando Python...\n')
                            sp.check_call([sys.executable,
                             os.path.join(current_path, m_issue.group(3))])
                        elif ext == '.sql':
                            sys.stdout.write('Ejecutando SQL...\n')
                            os.environ['PGPASSWORD'] = CONFIGURACION['password']
                            sp.check_call([os.path.join(CONFIG['pg_path'], 'psql'),
                             '-h', CONFIGURACION['host'],
                             '-U', CONFIGURACION['user'],
                             '-d', CONFIGURACION['db'],
                             '-f',
                             os.path.join(current_path, m_issue.group(3))])
                        f_done.write('%s\n' % current_issue)
                    except Exception as e:
                        sys.stderr.write(str(e))

    finally:
        f_todo.close()
        f_done.close()


if __name__ == '__main__':
    modo = 'post'
    if len(sys.argv) > 1:
        modo = sys.argv[1]
    actualizar(modo)