# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgversion/hgversion.py
# Compiled at: 2008-07-03 16:36:03
import binascii
repository = None
from mercurial import context, hg, node, repo, ui
try:
    repository = hg.repository(ui.ui(), '.')
except repo.RepoError:
    pass
else:
    current_ctx = context.changectx(repository)

    def info(ctx=current_ctx):
        return {'rev': ctx.rev(), 
           'node': ctx.node(), 
           'branch': ctx.branch(), 
           'tags': ctx.tags()}


    def close_non_tip_tag(ctx):
        ntt = non_tip_tag(ctx.tags())
        if ntt is not None:
            return ntt
        for parent in ctx.parents():
            ntt = non_tip_tag(parent.tags())
            if ntt is None:
                continue
            tagging_description = 'Added tag %s for changeset %s' % (ntt, node.short(parent.node()))
            if ctx.description() == tagging_description:
                return ntt

        return


    def non_tip_tag(tags):
        for tag in tags:
            if tag != 'tip':
                return tag

        return


    def most_recent_non_tip_tag(ctx):
        ntt = non_tip_tag(ctx.tags())
        if ntt is not None:
            return ntt
        if ctx.rev() >= 0:
            for parent in ctx.parents():
                ntt = most_recent_non_tip_tag(parent)
                if ntt is not None:
                    return ntt

        return


    def version():
        ntt = close_non_tip_tag(current_ctx)
        if ntt is not None:
            return ntt
        base_version = most_recent_non_tip_tag(current_ctx)
        if base_version is None:
            base_version = '0.0'
        i = info()
        return '%s-r%s_%s' % (base_version, i['rev'], binascii.hexlify(i['node']))