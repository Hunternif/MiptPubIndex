from django.db import models

class MiptDepartment(models.Model):
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200, blank=True)
  
  # The metric we assign to our departments:
  mipt_index = models.IntegerField(default=0)
  
  def __str__(self):
    return self.name_en


class Author(models.Model):
  author_id = models.CharField(max_length=50)
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200, blank=True)
  mipt_department = models.ForeignKey(MiptDepartment, blank=True, null=True)
  h_index = models.IntegerField(default=0)
  institute = models.CharField(max_length=200)
  
  def __str__(self):
    return "{}, {}".format(self.name_en, self.institute)


class Publication(models.Model):
  date = models.DateField()
  name_en = models.CharField(max_length=200)
  name_ru = models.CharField(max_length=200, blank=True)
  author = models.ManyToManyField(Author, blank=True, null=True)
  doi = models.CharField('Digital Object Identifier', max_length=100)
  citations = models.IntegerField(default=0)
  
  def __str__(self):
    return "{} {} ({} cit.)".format(self.name_en, self.date.year, self.citations)