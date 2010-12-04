from piston.handler import BaseHandler
from apps.research.models import Company 

class CompanyHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Company

    def read(self, request, company_id=None):
        if company_id:
            return Company.objects.get(id=company_id)

        else:
            return Company.objects.all()
