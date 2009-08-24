# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.core.management.base import BaseCommand
from tasks.importers import TaskImporter

def die(msg):
    print msg
    raise SystemExit

class Command(BaseCommand):
    """
    Daily import of CSV tasks.
    """
    can_import_settings = True
    
    def handle(self, source_file=None, *args, **kwargs):
        
        if not source_file:
            die('Source file required')

        file_path = os.path.abspath(source_file)

        if not os.path.isfile(file_path):
            die('Source file "%s" not found' % file_path)

        # Creates the importer and process the source file
        importer = TaskImporter(source=file_path)
        importer.parse()
            
        # Display errors
        for error in importer.errors:
            print 'Error importing item: description=%(description)s' % error['data']
            print error['exception']
            print '\n\n'
            
