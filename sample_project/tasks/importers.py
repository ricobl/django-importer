#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from django_importer.importers.csv_importer import CSVImporter
from tasks.models import Category, Task

# Equivalence for category slugs
category_map = {
    'Desenv': 'desenvolvimento',
    'Rede': 'rede',
    'Suporte': 'suporte',
}

class TaskImporter(CSVImporter):
    """
    CSV importer for tasks.
    """

    model = Task

    fields = ('category', 'date', 'start_time', 'end_time', 'duration',
              'description', 'template', 'temp_1', 'temp_2',
              'total_created', 'total_worked', 'total_closed',
              'total_to_test', 'total_open',
             )

    field_map = {
        'category': u'Categoria',

        'date': u'Date',
        'start_time': u'Inicio',
        'end_time': u'Fim',
        'duration': u'Duração',

        'description': u'Descrição',
        'template': u'Modelo',
        'temp_1': u'Temp1',
        'temp_2': u'Temp2',

        'total_created': u'Criadas',
        'total_worked': u'Trabalhadas',
        'total_closed': u'Fechadas',
        'total_to_test': u'To Test',
        'total_open': u'Open',
    }

    unique_fields = ('date', 'start_time')

    def parse_category(self, item, field_name, source_name):
        """
        Converts the text category to a tasks.Category instance.
        """
        # Get and checks for the corresponding slug
        slug = category_map.get(self.get_value(item, source_name), None)
        if not slug:
            return None
        # Load the category instance
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            pass

    def parse_date(self, item, field_name, source_name):
        """
        Converts the date in the format: Thu 03.

        As only the day is provided, tries to find the best match
        based on the current date, considering that dates are on
        the past.
        """
        # Get the current date
        now = datetime.now().date()
        # Get the date from the source
        val = self.get_value(item, source_name)
        week_day, day = val.split()
        day = int(day)
        # If the current date is minor than the item date
        # go back one month
        if now.day < day:
            if now.month == 1:
                now = now.replace(month=12, year=now.year-1)
            else:
                now = now.replace(month=now.month-1)
        # Finally, replace the source day in the current date
        # and return
        now = now.replace(day=day)
        return now

    def parse_totals(self, item, field_name, source_name):
        """
        Parse numeric fields.
        """
        val = self.get_value(item, source_name)
        try:
            return int(val)
        except:
            return 0

    # Reuse numeric parser method
    parse_total_created = parse_totals
    parse_total_worked = parse_totals
    parse_total_closed = parse_totals
    parse_total_to_test = parse_totals
    parse_total_open = parse_totals

