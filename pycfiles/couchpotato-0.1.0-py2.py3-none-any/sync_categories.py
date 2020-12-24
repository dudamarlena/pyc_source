# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchish/sync_categories.py
# Compiled at: 2009-02-21 07:15:53
import logging
log = logging.getLogger(__name__)

def sync(db, categories, remove_existing=False, update=False, verbose=False):
    """
    Allows the use of views similar to the following.
    
    function(doc) {
      if (doc.model_type == 'tour') {
        for (c in doc.categories) {
          var segments = doc.categories[c].split('.');
          for (s in segments) {
            var S = parseInt(s)+1;
             var segment = segments.slice(0,S);
            emit(segment, doc._id);
          } 
        }
    """
    if remove_existing == True:
        if verbose:
            print 'removing all existing categories'
        for row in db.view('category/all'):
            del db[row.id]

    flatcats = _accumulate_categories(categories, [], '')
    for (key, label) in flatcats:
        if update or len(db.view('_all_docs', startkey=key, endkey=key, limit=1)) == 0:
            cat = {'model_type': 'category', 'label': label, 'keys': key.split('.')}
            if update:
                if verbose:
                    print 'updating category (label,key): (%s,%s)' % (label, key)
                if key in db:
                    oldcat = db[key]
                    oldcat.update(cat)
                    cat = oldcat
            elif verbose:
                print 'initialising category (label,key): (%s,%s)' % (label, key)
            db[key] = cat


def _accumulate_categories(cats, flatcats, prefix):
    if cats is None:
        return flatcats
    else:
        for c in cats:
            for (category_key_label_tuple, subcats) in c.items():
                (cat_label, cat_key) = category_key_label_tuple.split(',')
                dotted_key = '%s%s' % (prefix, cat_key)
                flatcats.append((dotted_key, cat_label))
                _accumulate_categories(subcats, flatcats, '%s.' % dotted_key)

        return flatcats