# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django import template
from mpicore.models import *
#from django.shortcuts import render_to_response
import json




def faks(request):
  data_rows = []
  max_rank = 0
  for dep in MiptDepartment.objects.all():
    data_rows.append({"name": dep.name_ru, "rank": dep.rank})
    if dep.rank > max_rank:
      max_rank = dep.rank
  # Update percentages:
  data_rows.sort(key=lambda row: row['rank'], reverse=True)
  if max_rank > 0:
    for data_row in data_rows:
      data_row['percent'] = 100. * data_row['rank'] / max_rank
  return render(request, 'index.html', {"var1":"факультетам", "var2":"ФАКУЛЬТЕТЫ","rows": data_rows, "max_rank": max_rank})


def kafs(request):
  data_rows = []
  max_rank = 0
  for dep in MiptChair.objects.all():
    data_rows.append({"name": dep.name_ru, "rank": dep.rank})
    if dep.rank > max_rank:
      max_rank = dep.rank
  # Update percentages:
  data_rows.sort(key=lambda row: row['rank'], reverse=True)
  if max_rank > 0:
    for data_row in data_rows:
      data_row['percent'] = 100. * data_row['rank'] / max_rank
  return render(request, 'index.html', {"var1":"кафедрам", "var2":"КАФЕДРЫ","rows": data_rows, "max_rank": max_rank}) 




def rows(request):
  data_rows = []
  max_rank = 0
  for dep in MiptDepartment.objects.all():
    data_rows.append({"name": dep.name_ru, "rank": dep.rank})
    if dep.rank > max_rank:
      max_rank = dep.rank
  # Update percentages:
  data_rows.sort(key=lambda row: row['rank'], reverse=True)
  if max_rank > 0:
    for data_row in data_rows:
      data_row['percent'] = 100. * data_row['rank'] / max_rank
  
  return render(request, 'index.html', {"var1":"кафедрам", "var2":"КАФЕДРЫ","rows": data_rows, "max_rank": max_rank})


def affiliations(request):
  data_rows = []
  max_rank = 0
  for aff in Affiliation.objects.all():
    aff_total_citations = 0
    for pub in Publication.objects.filter(affiliation=aff):
      aff_total_citations += pub.citations
    data_rows.append({"name": aff.name_en, "rank": aff_total_citations})
    if aff_total_citations > max_rank:
      max_rank = aff_total_citations
  # Update percentages:
  if max_rank > 0:
    for data_row in data_rows:
      data_row['percent'] = 100. * data_row['rank'] / max_rank
  return render(request, 'index.html', {"var1":"аффилиациям", "var2":"АФФИЛИАЦИИ","rows": data_rows, "max_rank": max_rank})