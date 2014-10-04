from django.contrib import admin
from mpicore.models import Publication, Author, MiptDepartment

class AuthorInline(admin.TabularInline):
  model = Publication.author.through
  extra = 3

class PublicationAdmin(admin.ModelAdmin):
  inlines = (
    AuthorInline,
  )
  fields = ('date', 'name_en', 'name_ru', 'doi', 'citations')


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Author)
admin.site.register(MiptDepartment)