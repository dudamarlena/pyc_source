# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/pdf/diffs.py
# Compiled at: 2019-06-17 15:11:31
"""Utilities to assist with diffing PDF files."""
from __future__ import unicode_literals
from io import BytesIO
import diff_match_patch
from django.utils.encoding import force_bytes
from django.utils.six.moves import range
from pdfminer.converter import PDFConverter
from pdfminer.layout import LAParams, LTChar, LTContainer, LTText, LTTextLine
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

class BoundingBox(tuple):
    """The bounding box of some text.

    This is a 4-tuple, consisting of left, top, right, and bottom.
    """

    @staticmethod
    def union(a, b):
        """Return the union of two bounding boxes.

        Args:
            a (BoundingBox):
                The first bounding box.

            b (BoundingBox):
                The second bounding box.
        """
        if a is None:
            return b
        else:
            if b is None:
                return a
            else:
                return BoundingBox((
                 min(a[0], b[0]),
                 min(a[1], b[1]),
                 max(a[2], b[2]),
                 max(a[3], b[3])))

            return

    def __repr__(self):
        """Return a representation of this bounding box.

        Returns:
            unicode:
            A string representation of the bounding box.
        """
        return b'<BoundingBox left=%r top=%r right=%r bottom=%r>' % self


class LayoutData(object):
    """Data detailing the layout of a single PDF file.

    Attributes:
        content (unicode):
            The content of the document.

        line_map (list of int):
            A mapping between the content and which line each character is on.

        page_map (list of int):
            A mapping between the content and what page each character is on.

        bboxes (list of BoundingBox):
            A list of all the relevant bounding boxes in the document.

        bbox_map (list of int):
            A mapping between the content and the bounding boxes.
    """

    def __init__(self):
        """Initialize the object."""
        self.content = b''
        self.line_map = []
        self.page_map = []
        self.bboxes = []
        self.bbox_map = []
        self._content_parts = []
        self._current_page = -1
        self._current_line = -1
        self._current_bbox = -1

    def add_page(self):
        """Add a new page to the stored layout data."""
        self._current_page += 1

    def add_line(self):
        """Add a new line to the stored layout data."""
        self._current_line += 1

    def add_content(self, content, bbox):
        """Add content to the current page/line.

        Args:
            content (bytes):
                The content of the text.

            bbox (BoundingBox):
                The bounding box of the text.
        """
        if content:
            content = force_bytes(content)
            self._content_parts.append(content)
            self._current_bbox += 1
            self.bboxes.append(bbox)
            for i in range(len(content)):
                self.page_map.append(self._current_page)
                self.line_map.append(self._current_line)
                self.bbox_map.append(self._current_bbox)

        elif self._content_parts and self._content_parts[(-1)] != b' ':
            self._content_parts.append(b' ')
            self._current_bbox += 1
            self.bboxes.append(None)
            self.page_map.append(self._current_page)
            self.line_map.append(self._current_line)
            self.bbox_map.append(self._current_bbox)
        return

    def finalize(self):
        """Finalize the layout data."""
        self.content = (b'').join(self._content_parts)


class LayoutConverter(PDFConverter):
    """Layout converter for PDFMiner."""

    def __init__(self, layout, resource_manager):
        """Initialize the converter.

        Args:
            layout (LayoutData):
                The layout data object to write to.

            resource_manager (pdfminer.pdfinterp.PDFResourceManager):
                The PDFMiner resource manager.
        """
        super(LayoutConverter, self).__init__(resource_manager, BytesIO(), laparams=LAParams())
        self.layout = layout

    def receive_layout(self, ltpage):
        """Receive a page of layout from PDFMiner.

        Args:
            ltpage (pdfminer.layout.LTContainer):
                The page.
        """
        self.layout.add_page()
        self._render(ltpage)

    def _render(self, item):
        """Recurse into an item and store layout information.

        Args:
            item (pdfminer.layout.LTItem):
                The item to inspect. If this is text, store the layout
                information. If this is a container, recurse.
        """
        if isinstance(item, LTTextLine):
            self.layout.add_line()
            for child in item:
                self._render(child)

            self.layout.add_content(b'', None)
        elif isinstance(item, LTContainer):
            for child in item:
                self._render(child)

        elif isinstance(item, LTChar):
            self.layout.add_content(item.get_text().strip(), BoundingBox(item.bbox))
        elif isinstance(item, LTText):
            self.layout.add_content(item.get_text().strip(), None)
        return


def _extract_layout(attachment):
    """Extract the document layout from a given attachment.

    Args:
        attachment (reviewboard.attachments.models.FileAttachment):
            The file to extract the layout information from.

    Returns:
        LayoutData:
        The extracted layout.
    """
    try:
        attachment.file.open(mode=b'rb')
        resource_manager = PDFResourceManager()
        layout = LayoutData()
        device = LayoutConverter(layout, resource_manager)
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(attachment.file.file, maxpages=0):
            interpreter.process_page(page)

        device.close()
        layout.finalize()
        return layout
    finally:
        attachment.file.close()


def _compute_regions(op, layout, start, end, sync_page):
    """Compute the diff regions for a given diff chunk.

    This takes in a changed chunk from the text diff and correlates it with
    the layout data, returning a list of regions to draw overlays on.

    Args:
        op (unicode):
            The diff operation (insert or delete)

        layout (LayoutData):
            The layout data for the PDF file.

        start (int):
            The index into the layout data content corresponding to the
            start of the operation.

        end (int):
            The index into the layout data content corresponding to the end
            of the operation.

        sync_page (int):
            The number (0-indexed) of the page corresponding to the
            opposite side of the diff view where this operation took place.

    Yields:
        dict:
        Diff region data to send to the client.
    """
    last_bbox = None
    last_line = layout.line_map[start]
    last_page = layout.page_map[start]
    chunk_start = start
    initial_chunk = True
    for i in range(start, end):
        current_line = layout.line_map[i]
        if current_line != last_line:
            content = layout.content[chunk_start:i - 1].strip()
            if content:
                region = {b'bbox': last_bbox, 
                   b'op': op, 
                   b'page': last_page, 
                   b'syncPage': sync_page}
                if initial_chunk:
                    region[b'content'] = layout.content[start:end].strip()
                    initial_chunk = False
                yield region
            chunk_start = i
            last_bbox = layout.bboxes[layout.bbox_map[i]]
            last_line = current_line
            last_page = layout.page_map[i]
        else:
            last_bbox = BoundingBox.union(last_bbox, layout.bboxes[layout.bbox_map[i]])

    content = layout.content[chunk_start:end].strip()
    if content:
        region = {b'bbox': last_bbox, b'op': op, 
           b'page': last_page, 
           b'syncPage': sync_page}
        if initial_chunk:
            region[b'content'] = layout.content[start:end].strip()
        yield region
    return


def diff(old_file, new_file):
    """Perform a diff of two PDF files.

    Args:
        old_file (reviewboard.attachments.models.FileAttachment):
            The old version of the file.

        new_file (reviewboard.attachments.models.FileAttachment):
            The new version of the file.

    Returns:
        list of dict:
        A list of diff regions to be overlaid on the document view.
    """
    old_layout = _extract_layout(old_file)
    new_layout = _extract_layout(new_file)
    dmp = diff_match_patch.diff_match_patch()
    dmp.Diff_Timeout = 0
    diff_chunks = dmp.diff_main(old_layout.content, new_layout.content)
    dmp.diff_cleanupSemantic(diff_chunks)
    i1 = 0
    j1 = 0
    regions = []
    for op, chunk in diff_chunks:
        chunk_len = len(chunk)
        if op == dmp.DIFF_EQUAL:
            i1 += chunk_len
            j1 += chunk_len
        elif op == dmp.DIFF_DELETE:
            regions += _compute_regions(b'delete', old_layout, i1, i1 + chunk_len, new_layout.page_map[j1])
            i1 += chunk_len
        elif op == dmp.DIFF_INSERT:
            regions += _compute_regions(b'insert', new_layout, j1, j1 + chunk_len, old_layout.page_map[i1])
            j1 += chunk_len

    for region in regions:
        if region[b'op'] != b'insert' or b'content' not in region:
            continue
        for other_chunk in regions:
            if other_chunk[b'op'] == b'delete' and b'content' in other_chunk and region[b'content'] == other_chunk[b'content']:
                from_page = other_chunk[b'page']
                to_page = region[b'page']
                if from_page == to_page:
                    region[b'movedWithinPage'] = from_page
                    other_chunk[b'movedWithinPage'] = from_page
                else:
                    region[b'movedFromPage'] = from_page
                    other_chunk[b'movedToPage'] = to_page

    for region in regions:
        if b'content' in region:
            region[b'content'] = region[b'content'][:50]

    return regions


def make_diff_cache_key(old_file, new_file):
    """Return a cache key for storing diff data.

    Args:
        old_file (reviewboard.attachments.models.FileAttachment):
            The old version of the file.

        new_file (reviewboard.attachments.models.FileAttachment):
            The new version of the file.

    Returns:
        unicode:
        The cache key for storing the diff data.
    """
    return b'powerpack-pdf-diff-regions-%d-%d' % (
     old_file.pk, new_file.pk)