# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django import template
#from django.shortcuts import render_to_response
# Create your views here.

def tab(request):
    return render(request, 'index.html', {"x":"12", "y":"30"})

def rows(request):
    return render(request, 'index.html', {"rows":[[{"name":"автоматизированных биотехнических систем", "rait":"34"}],
    											  [{"name":"алгоритмов и технологий программирования", "rait":"48"}], 
    										      [{"name":"алгоритмов и технологий программирования", "rait":"100"}],
    										      [{"name":"автоматизированных биотехнических систем", "rait":"2"}],
    										      ]})

    
