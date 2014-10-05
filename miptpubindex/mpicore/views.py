from django.shortcuts import render
from django.http import HttpResponse
from django import template
from mpicore.models import MiptDepartment
#from django.shortcuts import render_to_response

def tab(request):
  return render(request, 'index.html', {"x":"12", "y":"30"})

def rows(request):
  data_rows = []
  max_rank = 0
  for dep in MiptDepartment.objects.all():
    dep_name = ''
    if len(dep.name_ru) == 0:
      dep_name = dep.name_en
    else:
      dep_name = dep.name_ru
    data_rows.append([{"name": dep_name, "rank": dep.mipt_index}])
    if dep.mipt_index > max_rank:
      max_rank = dep.mipt_index
  # Update percentages:
  if max_rank > 0:
    for data_row in data_rows:
      data_row[0]['percent'] = data_row[0]['rank'] / max_rank * 100
  
  return render(request, 'index.html', {"rows": data_rows, "max_rank": max_rank})
