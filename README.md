# django-importer

Importers for Django models.
Developed and maintained by Enrico Batista da Luz <rico.bl@gmail.com>

Provides basic functionality to import data into Django models, allowing easy
creation of custom importers. Highly extensible and customizable.

Data formats are commonly denormalized. The project doesn't aims to be the
"all-in-one" / "every-format" importer, but to provide a clean an flexible
interface to write custom importers.

# Features

  * currently supported formats: XML
  * easy to support new formats (CSV, Yaml, JSON, etc.)
  * maps source values to model fields
  * detects new / changed items
  * many hooks to customize the importer behaviour

# Usage

Actions speaks louder than words, so let's go ahead with a practical example.

Let's say you have a news application in your project and want to import data from a XML file:

    <data>
        <item>
            <id>1</id>
            <date>2009-04-20</date>
            <title>django-importer released</title>
            <content>Today, dango-importer has been released...</content>
        </item>
        ...
    </data>

The model definition:

    class Entry(models.Model):
        # External source ID, to keep track of already imported items
        external_id = models.IntegerField()
        # News entry properties
        headline = models.CharField(max_length=100)
        creation_date = models.DateTimeField()
        pub_date = models.DateTimeField()
        story = models.TextField()

Now the magic begins, let's write the importer. We must populate each field of our news
entry model, convert the creation date from string to a Python date and schedule the
publication date to the next hour.

    from django_importer.importers.xml import XmlImporter
    from datetime import datetime, timedelta

    class MyXmlImporter(XmlImporter):
        class Meta(XmlImporter.Meta):
            # XmlImporter specific meta property: the nodename that identifies an XML item
            item_tag_name = 'item'
            # A list of model field names expected to be imported from the source
            fields = ('external_id', 'headline', 'creation_date', 'story')
            # A dictionary mapping model field names to data source identifiers
            # In this case mappings points to XML nodes
            field_map = {'external_id': 'id',
                         'creation_date': 'date',
                         'headline': 'title',
                         'story': 'content',
                        }
            # List of fields that identifies an item as unique
            unique_fields = ('external_id',)
 
        def parse_creation_date(self, item, field_name, source_name):
            # Get the value `source_name` from the XML `item` for the field `field_name`
            # In other words: read the `date` node content to populate the field `creation_date` of our model.
            val = self.get_value(item, source_name)
            # Convert to a python date
            return datetime(*val.split('-'))

        def save_item(self, item, data, instance, commit=True):
            # If the item is new, setup a publication date
            if not instance.pk:
                instance.pub_date = datetime.now() + timedelta(hours=1)
            if commit:
                instance.save()
            return instance

And that's it. Now we can instantiate our importer and start parsing.

    from news.models import Entry
    from news.importers import MyXmlImporter

    importer = MyXmlImporter(Entry, 'path/to/source.xml')
    importer.parse()

