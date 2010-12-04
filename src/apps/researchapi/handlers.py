## python
import urllib
import decimal
import hashlib
from decimal import Decimal

## django
from django.conf import settings 
from django.core.cache import cache

## thirdparty django
from piston.handler import BaseHandler

## interapp
from apps.research.models import Company, Product

## module globals
ONE_DAY = settings.ONE_DAY
MAX_COMPARABLE_COMPANIES = settings.MAX_COMPARABLE_COMPANIES 

## module utils
def _rating_rounding(val):
    return Decimal(str(val)).quantize(Decimal('.01'), rounding=decimal.ROUND_HALF_EVEN)

def _round_company_rating(company):
    val = company.total_weighted_rating 
    rounded = Decimal(str(val)).quantize(Decimal('.01'), rounding=decimal.ROUND_HALF_EVEN)
    company.total_weighted_rating = rounded

    if company.parent:
        _round_company_rating(company.parent)

def _get_hashkey(prefix, query_term):
    return hashlib.md5('%s.%s' % (prefix, query_term,)).hexdigest()

## handler classes
class CompanyHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Company

    def read(self, request, company_name):
        company_name = urllib.unquote_plus(company_name)

        # caching
        hashkey = _get_hashkey('company', company_name)
        cached_result = cache.get(hashkey)

        if cached_result: 
            return cached_result

        company = Company.objects.filter(name__icontains=company_name)[:1]
        if len(company) < 1:    
            # return empty set
            return [] 

        company = company[0]
        _round_company_rating(company)

        alternatives = Company.objects.filter(industry__in=company.industry.all(), 
            total_weighted_rating__gt=company.total_weighted_rating) \
            .order_by('-total_weighted_rating')[:MAX_COMPARABLE_COMPANIES]

        for an_alternative in alternatives:
            _round_company_rating(an_alternative)

        res = {
            'company' : company,
            'alternatives' : alternatives,
        }

        # caching
        cache.set(hashkey, res, ONE_DAY)

        return res


class SearchHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Product

    def read(self, request, search_term):
        search_term = urllib.unquote_plus(search_term)

        # caching
        hashkey = _get_hashkey('company', search_term)
        cached_result = cache.get(hashkey)

        if cached_result: 
            return cached_result

        company_list = list(Company.objects.filter(name__icontains=search_term))
        for company in company_list: _round_company_rating(company)

        product_list = list(Product.objects.filter(name__icontains=search_term))
        for product in product_list:
            _round_company_rating(product.company)

        res = {
            'companies' : company_list,
            'products' : product_list
        }

        cache.set(hashkey, res, ONE_DAY)

        return res
