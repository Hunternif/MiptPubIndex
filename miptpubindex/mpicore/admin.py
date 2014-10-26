from django.contrib import admin
from mpicore.models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models.aggregates import Count

class PublicationSpecialCases(admin.SimpleListFilter):
    title = _('Special cases')
    parameter_name = 'SpecialCase'
    def lookups(self, request, model_admin):
        return (
            ('NoAff', _('No affiliations')),
            ('NoAuthors', _('No authors')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'NoAff':
            return queryset.annotate(aff_count=Count('affiliation')).filter(aff_count=0)
        if self.value() == 'NoAuthors':
            return queryset.annotate(auth_count=Count('author')).filter(auth_count=0)
        
class AuthorInline(admin.TabularInline):
  model = Publication.author.through
  extra = 3

class AffiliationInline(admin.TabularInline):
  model = Publication.affiliation.through
  extra = 2

class AffiliationAdmin(admin.ModelAdmin):
    search_fields = ['af_id','name_en']
    
class PublicationAdmin(admin.ModelAdmin):
  inlines = (
    AuthorInline,
    AffiliationInline
  )
  fields = ('date', 'name_en', 'name_ru', 'eid', 'doi', 'journal', 'citations')
  search_fields = ['eid','name_en']
  list_filter = (PublicationSpecialCases,)

admin.site.register(Journal)
admin.site.register(Affiliation, AffiliationAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Author)
admin.site.register(MiptDepartment)
admin.site.register(MiptChair)