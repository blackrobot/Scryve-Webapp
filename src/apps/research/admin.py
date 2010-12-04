from django.contrib import admin
from django import forms

from apps.research.models import *

class RatingInline(admin.TabularInline):
    model = Rating

class CompanyAdmin(admin.ModelAdmin):
    inlines = (RatingInline, )
    list_display = ('name', 'total_weighted_rating', 'parent' )
    search_fields = ('name', 'parent__name')

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    list_editable = ('weight',)
    list_filter = ('category', 'industry')

admin.site.register(IndicatorCategory)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(IndicatorRatingOption)
admin.site.register(Industry)
admin.site.register(Company, CompanyAdmin)
