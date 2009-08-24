#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class Category(models.Model):
    name = models.CharField('name', max_length=64)
    slug = models.SlugField('slug', max_length=64)

    class Meta:
        verbose_name = 'category'

    def __unicode__(self):
        return u'%s' % self.slug

class Task(models.Model):
    category = models.ForeignKey(Category)

    date = models.DateField('date')
    start_time = models.TimeField('start time')
    end_time = models.TimeField('end time')
    duration = models.TimeField('duration')

    description = models.CharField('description', max_length=124)
    template = models.CharField('template', max_length=124)
    temp_1 = models.CharField('temp 1', max_length=64)
    temp_2 = models.CharField('temp 2', max_length=64)

    total_created = models.PositiveSmallIntegerField('total created', null=True, blank=True)
    total_worked = models.PositiveSmallIntegerField('total worked', null=True, blank=True)
    total_closed = models.PositiveSmallIntegerField('total closed', null=True, blank=True)
    total_to_test = models.PositiveSmallIntegerField('total to test', null=True, blank=True)
    total_open = models.PositiveSmallIntegerField('total open', null=True, blank=True)

    class Meta:
        verbose_name = 'task'

    def __unicode__(self):
        return u'%s' % self.description

