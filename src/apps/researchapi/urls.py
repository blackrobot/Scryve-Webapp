from django.conf.urls.defaults import *
from piston.resource import Resource
from apps.researchapi.handlers import CompanyHandler, SearchHandler

company_handler = Resource(CompanyHandler)
search_handler = Resource(SearchHandler)

urlpatterns = patterns('',
    url('^company/(?P<company_name>[^/]+)/', company_handler),
    url('^search/(?P<search_term>[^/]+)/', search_handler)
)
