from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from piston.resource import Resource
from apps.researchapi.handlers import CompanyHandler, SearchHandler

company_handler = Resource(CompanyHandler)
search_handler = Resource(SearchHandler)

urlpatterns = patterns('',
    url('^company/(?P<company_name>[^/]+)/', company_handler),
    url('^search/(?P<search_term>[^/]+)/', search_handler),
    url('^$', direct_to_template, { 'template': 'index.html' }),
)
