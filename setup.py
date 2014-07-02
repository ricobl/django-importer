#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <django-importer - Importers for Django models>
# Copyright (C) <2009>  Enrico Batista da Luz <rico.bl@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django_importer import version
from setuptools import setup

setup(
    name='django-importer',
    version=version,
    description='Data importers for Django models',
    author=u'Enrico Batista da Luz',
    author_email='rico.bl@gmail.com',
    url='http://github.com/ricobl/django-importer/',
    packages=['django_importer', 'django_importer.importers'],
)

