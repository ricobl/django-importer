# Sample Project

There's a sample project demonstrating the use of `django_importer` in
a management command to import data from a CSV file to a django model.

# Testing

To manually test the command, go to the `sample_project` directory,
open the shell and check the number of Tasks:

    ./manage.py shell
    >>> from tasks.models import Task
    >>> Task.objects.count()
    0

Now run the import command using the sample CSV file and check the
number of Tasks again:

    ./manage.py tasks_import_daily tasks.csv
    ./manage.py shell
    >>> from tasks.models import Task
    >>> Task.objects.count()
    21

