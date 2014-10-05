# -*- coding: utf-8 -*-
from django.db import models

class MiptDepartment(models.Model):
  '''Факультет МФТИ'''
  name_en = models.CharField(max_length=500, blank=True)
  name_ru = models.CharField(max_length=500)
  
  # The metric we assign to our departments & chairs:
  rank = models.IntegerField(default=0)
  
  def __str__(self):
    return self.name_ru


class MiptChair(models.Model):
  '''Базовая кафедра МФТИ'''
  name_en = models.CharField(max_length=500, blank=True)
  name_ru = models.CharField(max_length=500)
  department = models.ForeignKey(MiptDepartment)
  
  # The metric we assign to our departments & chairs:
  rank = models.IntegerField(default=0)
  
  def __str__(self):
    return self.name_ru


class Author(models.Model):
  author_id = models.CharField(max_length=50)
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200, blank=True)
  mipt_chair = models.ForeignKey(MiptChair, blank=True, null=True)
  h_index = models.IntegerField(default=0)
  institute = models.CharField(max_length=200)
  
  def __str__(self):
    return "{}, {}".format(self.name_en, self.institute)


class Journal(models.Model):
  issn = models.CharField('ISSN', max_length=50)
  name_en = models.CharField(max_length=200)
  rank_sjr = models.FloatField('SJR (SCImago Journal Rank)', default=0)
  rank_snip = models.FloatField('SNIP (Source Normalized Impact per Paper)', default=0)
  
  def __str__(self):
    return self.name_en


class Publication(models.Model):
  date = models.DateField()
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200, blank=True)
  author = models.ManyToManyField(Author, blank=True, null=True)
  doi = models.CharField('DOI (Digital Object Identifier)', max_length=100)
  citations = models.IntegerField(default=0)
  journal = models.ForeignKey(Journal)
  
  def __str__(self):
    return "{} {} ({} cit.)".format(self.name_en, self.date.year, self.citations)