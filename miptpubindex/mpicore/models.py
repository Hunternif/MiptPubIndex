from django.db import models

class MiptDepartment(models.Model):
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200)
  mipt_index = models.IntegerField(default=0)
  
  def __str__(self):
    return self.name_en

class Publication(models.Model):
  date = models.DateField()
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200)
  doi = models.CharField('Digital Object Identifier', max_length=100)
  citations = models.IntegerField(default=0)
  
  def __str__(self):
    return ": ".join(self.name_en, str(citations))

class Author(models.Model):
  author_id = models.CharField(max_length=50)
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200)
  mipt_department = models.ForeignKey(MiptDepartment)
  publication = models.ForeignKey(Publication)
  h_index = models.IntegerField(default=0)
  institute = models.CharField(max_length=200)
  
  def __str__(self):
    return ", ".join(self.name_en, str(mipt_department))