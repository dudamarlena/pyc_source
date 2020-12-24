# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/phial/processor.py
# Compiled at: 2014-04-22 23:03:09
from . import exceptions
from . import pages
from . import documents
from . import utils
import errno, inspect, os, shutil, stat, logging
log = logging.getLogger(__name__)

def _mkdirs(dir_path):
    """Creates a directory and its parents if they don't exist."""
    try:
        os.makedirs(dir_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def process(source_dir='./site', output_dir='./output', index_path='.phial_index'):
    """
    Processes all of the pages in your site appropriately. This is the function
    the drives the generation of a Phial site and is what is run when you use
    the Phial command line tool.

    """
    artifacts = render_site(source_dir)
    finalize_paths(artifacts, source_dir, output_dir)
    if index_path is not None:
        index_path = os.path.join(output_dir, index_path)
        clean_output_dir(output_dir, index_path)
    output_site(artifacts)
    if index_path is not None:
        write_index(artifacts, output_dir, index_path)
    return


def write_index(artifacts, output_dir, index_path):
    with open(index_path, 'w') as (f):
        for i in artifacts:
            print >> f, os.path.relpath(i._target_path, output_dir)


def clean_output_dir(output_dir, index_path):
    old_files = []
    try:
        f = open(index_path)
    except IOError as e:
        log.debug('Could not open Phial index at %r: %r', index_path, e)
        return

    output_dir = os.path.abspath(output_dir)
    with f:
        for i in f:
            i = i.strip()
            path = os.path.join(output_dir, i)
            if not os.path.abspath(path).startswith(output_dir):
                raise RuntimeError(('invalid path in index: {!r}').format(i))
            try:
                mode = os.stat(path).st_mode
            except OSError as e:
                if e.errno == errno.ENOENT:
                    log.warning('Entry in Phial index does not exist: %r', os.path.relpath(path))
                    continue

            if stat.S_ISREG(mode):
                old_files.append(path)

    old_directories = set()
    for i in old_files:
        old_directories.add(os.path.dirname(i))
        os.remove(i)

    for i in old_directories:
        try:
            os.removedirs(i)
        except OSError:
            pass

    log.debug('Cleaned output directory. Deleted files %r. Deleted directories %r.', [ os.path.relpath(i) for i in old_files ], [ os.path.relpath(i) for i in old_directories ])


def render_site(source_dir):
    """
    Calls the page functions of all registered pages as well as resolving all
    of the registered assets.

    :param source_dir: The source directory to change into.

    :returns: A list of artifacts (RenderedPage and ResolvedAsset objects).

    .. warning::

        This function changes the current directory using ``os.chdir()``. Be
        wary of using this function in a multi-threaded application. It changes
        it back to its previous value right before the function returns.

    """
    old_cwd = os.getcwd()
    os.chdir(source_dir)
    artifacts = []
    for i in pages._pages:
        artifacts += render_page(i)

    for i in pages._assets:
        artifacts += resolve_asset(i)

    os.chdir(old_cwd)
    return artifacts


def finalize_paths(artifacts, source_dir, output_dir):
    """
    Figures out exactly where on the filesystem the artifacts' targets and
    sources (if applicable) are located.

    :param artifacts: A list of artifacts to look at. This list will be
            modified in place and each artifact will have appropriate
            ``_target_path`` and ``_source_path`` attributes set.
    :param source_dir: The source directory as provided by the user.
    :param output_dir: The output directory as provided by the user.

    :returns: None

    """
    source_dir = os.path.abspath(source_dir)
    output_dir = os.path.abspath(output_dir)
    for i in artifacts:
        i._target_path = os.path.abspath(os.path.join(output_dir, i.target))
        if not i._target_path.startswith(output_dir):
            log.error("Artifact's target is outside of the output directory: %r", i)
            raise RuntimeError('Artifact target is outside output directory.')
        if isinstance(i, pages.ResolvedAsset):
            i._source_path = os.path.abspath(os.path.join(source_dir, i.source))
            if not i._source_path.startswith(source_dir):
                log.error("Artifact's source is outside of source directory: %r", i)
                raise RuntimeError('Artifact source is outside source directory.')


def output_site(artifacts):
    """
    Outputs the site.

    :param artifacts: A list of artifacts that have already been sent through
            finalize_paths().

    :returns: None

    """
    for i in artifacts:
        _mkdirs(os.path.dirname(i._target_path))
        if isinstance(i, pages.RenderedPage):
            with open(i._target_path, 'w') as (f):
                if isinstance(i.content, unicode):
                    f.write(i.content.encode('utf_8'))
                else:
                    f.write(i.content)
        else:
            shutil.copy(i._source_path, i._target_path)


def _resolve_target(raw_target, source):
    """
    Resolves a target string with the provided source.

    :param raw_target: The unresolved target string (ex:
            ``projects/{name}.htm``)
    :param source: A Document instance or a file path (the same as what gets
            passed to a Page's func).

    :returns: The resulting file path.

    """
    target_info = {}
    if source is not None:
        if isinstance(source, documents.Document):
            source_path = source.file_path
            target_info['frontmatter'] = source.frontmatter
        else:
            source_path = source
        target_info.update({'path': source_path, 
           'dir': os.path.dirname(source_path), 
           'fullname': os.path.basename(source_path), 
           'name': os.path.splitext(os.path.basename(source_path))[0]})
    return raw_target.format(**target_info)


def _resolve_result(result, page, source):
    """
    Takes a result as returned by a page function and transforms it into an
    appropriate RenderedPage or ResolvedAsset object.

    :param result: The return value of a page function.
    :param page: The page object housing that page function.
    :param source: The source provided to the page function. May be ``None``
            to imply that a source was not provided.

    :returns: A RenderedPage or ResolvedAsset object.

    """
    if not isinstance(result, (pages.RenderedPage, pages.ResolvedAsset)):
        result = pages.RenderedPage(target=None, content=result)
    if result.target is None and page.target is not None:
        result.target = _resolve_target(page.target, source)
    if result.target is None and source is not None:
        if isinstance(source, documents.Document):
            result.target = source.file_path
        else:
            result.target = source
    if result.target is None:
        raise RuntimeError(('not enough informaton to resolve target for {!r}').format(page))
    return result


def render_page(page):
    """
    Renders a single page.

    :returns: A list of RenderedPage and/or ResolvedAsset objects.

    """
    argspec = inspect.getargspec(page.func)
    arguments = set(argspec.args)

    def filter_args(dictionary):
        """Returns a dictionary containing only keys in ``arguments``."""
        if argspec.keywords is not None:
            return dictionary
        else:
            return dict(i for i in dictionary.items() if i[0] in arguments)

    results = []
    if page.files is None:
        potential_args = {'self': page, 'target': page.target}
        result = page.func(**filter_args(potential_args))
        result = _resolve_result(result, page, None)
        results.append(result)
    else:
        for path in utils.glob_files(page.files):
            if page.parse_files:
                source = documents.Document(path)
            else:
                source = path
            potential_args = {'self': page, 
               'source': source, 
               'target': _resolve_target(page.target, source)}
            result = page.func(**filter_args(potential_args))
            if result is None:
                continue
            result = _resolve_result(result, page, source)
            results.append(result)

    return results


def resolve_asset(asset):
    """
    Resolves a single asset.

    :returns: A list of ResolvedAsset objects.

    """
    results = []
    for path in utils.glob_files(asset.files):
        resolved = pages.ResolvedAsset(target=None, source=path)
        if asset.target is not None:
            resolved.target = _resolve_target(asset.target, path)
        else:
            resolved.target = path
        results.append(resolved)

    return results