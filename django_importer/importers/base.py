# -*- coding: utf-8 -*-

"""
= django-importer =

Importers for Django models.
Developed and maintained by Enrico Batista da Luz <rico.bl@gmail.com>

To use an existent importer, configure the class properties:

  * `model`: the model to create instances from the data.
  * `fields`: which fields in your model you want to import from the source.
  * `field_map`: the mapping of your field models to the source fields.
  * `unique_fields`: fields that identify an item as unique.

To create your own importer for a different source type, extend `ImporterBase`
and all methods with `NotImplementedError`. Or extend one of the available
importers.
"""

from traceback import format_exception
import sys

class Importer(object):
    """
    Base class to create importers for different sources.
    """
    
    fields = ()
    field_map = {}
    unique_fields = ()
    model = None
    
    def __init__(self, source=None):
        self.source = source
        self.loaded = False
        self.errors = []
    
    def save_error(self, data, exception_info):
        """
        Saves an error in the error list. 
        """
        # TODO: what to do with errors? Let it flow? Write to a log file?
        self.errors.append({'data': data,
                            'exception': ''.join(format_exception(*exception_info)),
                            })
    
    def parse(self):
        """
        Parses all data from the source, saving model instances.
        """
        # Checks if the source is loaded
        if not self.loaded:
            self.load(self.source)
        
        for item in self.get_items():
            # Parse the fields from the source into a dict
            data = self.parse_item(item)
            # Get the instance from the DB, or a new one
            instance = self.get_instance(data)
            # Feed instance with data
            self.feed_instance(data, instance)
            # Try to save the instance or keep the error
            try:
                self.save_item(item, data, instance)
            except Exception as e:
                self.save_error(data, sys.exc_info())

        # Unload the source
        self.unload()
    
    def parse_item(self, item):
        """
        Receives an item and returns a dictionary of field values.
        """
        # Create a dictionary from values for each field
        parsed_data = {}
        
        for field_name in self.fields:
            # A field-name may be mapped to another identifier on the source,
            # it could be a XML path or a CSV column name / position.
            # Defaults to the field-name itself.
            source_name = self.field_map.get(field_name, field_name)
            
            # Uses a custom method "parse_%(field_name)"
            # or get the value from the item
            parse = getattr(self, 'parse_%s' % field_name, None)
            if parse:
                value = parse(item, field_name, source_name)
            else:
                value = self.get_value(item, source_name)
                
            # Add the value to the parsed data
            parsed_data[field_name] = value
        return parsed_data
    
    def get_instance(self, data):
        """
        Get an item from the database or an empty one if not found.
        """
        # Get unique fields
        unique_fields = self.unique_fields
        
        # If there are no unique fields option, all items are new
        if not unique_fields:
            return self.model()
        
        # Build the filter
        filter = dict([(f, data[f]) for f in unique_fields])
        
        # Get the instance from the DB or use a new instance
        try:
            instance = self.model._default_manager.get(**filter)
        except self.model.DoesNotExist:
            return self.model()
        
        return instance
    
    def feed_instance(self, data, instance):
        """
        Feeds a model instance using parsed data (usually from `parse_item`).
        """
        for prop, val in data.items():
            setattr(instance, prop, val)
        return instance
    
    def save_item(self, item, data, instance, commit=True):
        """
        Saves a model instance to the database.
        """
        if commit:
            instance.save()
        return instance
    
    def unload(self):
        """
        Unloads the source file.
        Useful to close open files and free resources.

        Not a required method by subclasses.

        Rembember to unset the ``loaded`` when extending this method.
        """
        self.loaded = False
    
    ### ABSTRACT METHODS #############
    
    def load(self, source):
        """
        Load data from the source.
        
        Must be implemented on subclasses or will raise `NotImplementedError`.
        """
        raise NotImplementedError

    def get_items(self):
        """
        Get the list of items for the current source.
        Must return an iterable.
        
        Must be implemented on subclasses or will raise `NotImplementedError`.
        """
        raise NotImplementedError
    
    def get_value(self, item, source_name):
        """
        Receives an item from the source and a source name,
        and must return the value for the field.
        
        Must be implemented on subclasses or will raise `NotImplementedError`.
        """
        raise NotImplementedError

