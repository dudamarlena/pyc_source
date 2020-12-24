# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/pypi_rankings/crawlers/dependencies.py
# Compiled at: 2015-02-17 04:35:44
import os, json, shutil, tarfile, zipfile, tempfile, time, multiprocessing
from urllib import urlretrieve
from infi.execute import execute_assert_success
from progress import Progress
PROCESS_COUNT = 5

def extract_tar(fname):
    if fname.endswith('gz'):
        tfile = tarfile.open(fname, 'r:gz')
        names = tfile.getnames()
    elif fname.endswith('.zip'):
        tfile = zipfile.ZipFile(fname)
        names = tfile.namelist()
    else:
        return
    dirnames = set([ tfname.lstrip('./').split('/')[0] for tfname in names ])
    nodirs = all('/' not in name for name in names)
    if len(dirnames) > 1 or nodirs:
        os.mkdir('package_dir')
        tfile.extractall('package_dir')
    else:
        tfile.extractall('.')


def get_dependencies(url):
    tmpdir = tempfile.mkdtemp()
    try:
        os.chdir(tmpdir)
        fname, _ = urlretrieve(url)
        try:
            extract_tar(fname)
            new_dirs = [ d for d in os.listdir('.') if os.path.isdir(d) ]
            setup_executor = os.path.join(os.path.dirname(__file__), 'setup_executor.py')
            shutil.copy(setup_executor, new_dirs[0])
            os.chdir(new_dirs[0])
            output = execute_assert_success(['python', 'setup_executor.py'], timeout=300).get_stdout().strip()
            res = eval(output.splitlines()[(-1)])
            return res
        finally:
            os.remove(fname)

    finally:
        shutil.rmtree(tmpdir)


def per_package(package, url):
    try:
        return (
         package, get_dependencies(url))
    except (IndexError, ValueError):
        return
    except Exception as e:
        return

    return


def save_package_data(conn, package, dependencies, real_package_lookup):
    conn.execute('DELETE FROM dependencies WHERE name=?', (package,))
    conn.execute('REPLACE INTO dependencies(name, raw_dependencies, crawl_time) VALUES (?, ?, ?)', (
     package, json.dumps(dependencies) if dependencies is not None else None, time.time()))
    if dependencies is not None:
        for dependency in dependencies:
            if isinstance(dependency, basestring) and len(dependency) > 0:
                dependency = dependency.split('>')[0].split('<')[(-1)].split('=')[0].strip().lower()
                if dependency in real_package_lookup:
                    real_dependency = real_package_lookup[dependency]
                    conn.execute('REPLACE INTO dependencies(name, dependency) VALUES (?, ?)', (
                     package, real_dependency))

    conn.commit()
    return


def crawl(conn, crawl_count=1, new_only=True):
    all_packages = set(x[0] for x in conn.execute('SELECT name FROM packages'))
    real_package_lookup = dict((package_name.lower(), package_name) for package_name in all_packages)
    package_query = 'SELECT name, latest_sdist FROM packages WHERE latest_sdist IS NOT NULL'
    if new_only:
        package_query += ' AND name NOT IN (SELECT DISTINCT name FROM dependencies)'
    packages = list(conn.execute(package_query))
    total_count = len(packages)
    progress = Progress('dependencies', crawl_count, total_count)
    progress.start()
    mutex = multiprocessing.Lock()

    def package_callback(result):
        from . import get_conn
        mutex.acquire()
        try:
            progress.parse_count += 1
            if result is None:
                return
            package, dependencies = result
            conn = get_conn()
            save_package_data(conn, package, dependencies, real_package_lookup)
        finally:
            mutex.release()

        return

    pool = multiprocessing.Pool(PROCESS_COUNT)
    for package, url in packages:
        pool.apply_async(per_package, args=(package, url), callback=package_callback)

    pool.close()
    pool.join()
    progress.stop()


if __name__ == '__main__':
    from . import get_conn
    conn = get_conn()
    crawl(conn, new_only=False)