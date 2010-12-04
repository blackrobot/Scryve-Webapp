from django.conf.urls.defaults import *
from piston.resource import Resource
from apps.researchapi.handlers import CompanyHandler

company_handler = Resource(CompanyHandler)

urlpatterns = patterns('',
    url(r'company/(?P<company_id>\d+)', company_handler),
    url(r'companies', company_handler)
)
