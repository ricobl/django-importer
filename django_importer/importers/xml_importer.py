# -*- coding: utf-8 -*-

from django_importer.importers.base import Importer
from django.utils.encoding import smart_str

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

# Try to import the best match for `ElementTree`.
# Prioritizes the C port `cElementTree` for *much* better performance.
# Starting from Python 2.5, `cElementTree` is found on `xml.etree`
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    try:
        import cElementTree as ElementTree
    except ImportError:
        from elementtree import ElementTree

class XMLImporter(Importer):
    """
    Import models from a local XML file. Requires `ElementTree`.
    """

    # The name of the XML node that represents an item
    item_tag_name = 'item'

    def load(self, source):
        """
        Doesn't load anything, just changes the source property,
        `ElementTree` is capable of using a file stream or path,
        so the source type doesn't matter.
        """
        self.source = source
        self.loaded = True

    def get_items(self):
        """
        Iterator of the list of items in the XML source.
        """
        # Use `iterparse`, it's more efficient, specially for big files
        for event, item in ElementTree.iterparse(self.source):
            if item.tag == self.item_tag_name:
                yield item
                # Releases the item from memory
                item.clear()

    def get_value(self, item, source_name):
        """
        This method receives an item from the source and a source name,
        and returns the text content for the `source_name` node.
        """
        return force_text(smart_str(item.findtext(source_name))).strip()

