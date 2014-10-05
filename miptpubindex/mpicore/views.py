# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django import template
from mpicore.models import MiptDepartment
#from django.shortcuts import render_to_response
import json




def faks(request):
  data_rows = []
  max_rank = 0
  for dep in MiptDepartment.objects.all():
    data_rows.append([{"name": dep.name_ru, "rank": dep.rank}])
    if dep.rank > max_rank:
      max_rank = dep.rank
  # Update percentages:
  if max_rank > 0:
    for data_row in data_rows:
      data_row[0]['percent'] = 100. * data_row[0]['rank'] / max_rank
  return render(request, 'index.html', {"var1":"факультетам", "var2":"ФАКУЛЬТЕТЫ","rows": data_rows, "max_rank": max_rank})


def kafs(request):
  data_rows = []
  max_rank = 0
  for dep in MiptDepartment.objects.all():
    data_rows.append([{"name": dep.name_ru, "rank": dep.rank}])
    if dep.rank > max_rank:
      max_rank = dep.rank
  # Update percentages:
  if max_rank > 0:
    for data_row in data_rows:
      data_row[0]['percent'] = 100. * data_row[0]['rank'] / max_rank
  return render(request, 'index.html', {"var1":"кафедрам", "var2":"КАФЕДРЫ"}) 




def rows(request):
  data_rows = []
  max_rank = 0
  for dep in MiptDepartment.objects.all():
    data_rows.append([{"name": dep.name_ru, "rank": dep.rank}])
    if dep.rank > max_rank:
      max_rank = dep.rank
  # Update percentages:
  if max_rank > 0:
    for data_row in data_rows:
      data_row[0]['percent'] = 100. * data_row[0]['rank'] / max_rank
  
  return render(request, 'index.html', {"var1":"кафедрам", "var2":"КАФЕДРЫ","rows": data_rows, "max_rank": max_rank})
