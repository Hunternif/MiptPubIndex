from django.contrib import admin
from mpicore.models import *

class AuthorInline(admin.TabularInline):
  model = Publication.author.through
  extra = 3

class AffiliationInline(admin.TabularInline):
  model = Publication.affiliation.through
  extra = 2

class PublicationAdmin(admin.ModelAdmin):
  inlines = (
    AuthorInline,
    AffiliationInline
  )
  fields = ('date', 'name_en', 'name_ru', 'eid', 'doi', 'journal', 'citations')


admin.site.register(Journal)
admin.site.register(Affiliation)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Author)
admin.site.register(MiptDepartment)
admin.site.register(MiptChair)