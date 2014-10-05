# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'miptpubindex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^do1/', "mpicore.views.rows"),
    url(r'^tab/fak', "mpicore.views.faks"),
    url(r'^tab/kaf', "mpicore.views.kafs"),
    url(r'^tab/aff', "mpicore.views.affiliations"),
)