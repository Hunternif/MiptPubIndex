from django.contrib import admin
from mpicore.models import Publication, Author, MiptDepartment

# Register your models here.
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(MiptDepartment)