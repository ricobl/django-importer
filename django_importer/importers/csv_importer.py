# -*- coding: utf-8 -*-

import csv
from django_importer.importers.base import Importer
from django.utils.encoding import smart_str, force_unicode

def convert_string(s):
    return force_unicode(smart_str(s)).strip()

class CSVImporter(Importer):
    """
    Import models from a local CSV file. Requires `csv` module.
    """
    
    def load(self, source):
        """
        Opens the source file.
        """
        self.source = open(self.source, 'rb')    
        self.loaded = True

    def unload(self):
        """
        Closes the input file to free resources.
        """
        self.source.close()
        self.loaded = False

    def get_items(self):
        """
        Iterator to read the rows of the CSV file.
        """
        # Get the csv reader
        reader = csv.reader(self.source)
        # Get the headers from the first line
        headers = reader.next()
        # Read each line yielding a dictionary mapping
        # the column headers to the row values
        for row in reader:
            # Skip empty rows
            if not row:
                continue
            yield dict(zip(headers, row))
    
    def get_value(self, item, source_name):
        """
        This method receives an item from the source and a source name,
        and returns the text content for the `source_name` node.
        """
        val = item.get(source_name.encode('utf-8'), None)
        if val is not None:
            val = convert_string(val)
        return val

