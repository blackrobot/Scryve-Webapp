import csv
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.db.models import Sum
# from django.core.urlresolvers import reverse

from apps.research.models import *
from apps.research.forms import *


def handle_csv(file):
    # Open the CSV file and save it to the filesystem
    path = "%s/csv/%s.csv" % (settings.MEDIA_ROOT, datetime.datetime.now())
    destination = open(path, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()

    return csv.reader(open(path), delimiter=',', quotechar='"')

def handle_research_csv(file):
    csv_file = handle_csv(file)

    industry = None
    current_company = None

    for row in csv_file:
        if settings.DEBUG:
            print "Processing line: %d" % csv_file.line_num

        if csv_file.line_num == 1:
            industry_name = row[0]
            industry = Industry.objects.get_or_create(name=industry_name)[0]
        elif csv_file.line_num == 2:
            order = ["Company Name","Indicator ","Category","Explanation","Rating","Source","Subsidiary","Product"]
            # indicator, explanation, rating, source, product
            for x in range(0, len(order)):
                if order[x] != row[x]:
                    return False
        else:
            items = {
                "company name": row[0],
                "indicator": row[1],
                "category": row[2],
                "explanation": row[3],
                "rating": row[4],
                "source": row[5] if row[5] != "" else None,
                "subsidiary": row[6] if row[6] != "" else None,
                "product": row[7] if row[7] != "" else None,
            }

            if items["company name"] != "":
                category = IndicatorCategory.objects.get_or_create(name=items["category"])[0]

                if items["subsidiary"]:
                    parent_company = Company.objects.get_or_create(name=items["company name"])[0]
                    company = Company.objects.get_or_create(name=items["subsidiary"], parent=parent_company)[0]
                    company.industry.add(industry)
                else:
                    company = Company.objects.get_or_create(name=items["company name"])[0]
                    company.industry.add(industry)
                company.save()

                indicator = Indicator.objects.get(name=items["indicator"], category=category, industry=industry)

                rating_option = IndicatorRatingOption.objects.get(
                    indicator=indicator,
                    description=items["rating"],
                )

                rating = Rating.objects.create(
                    rating=rating_option,
                    explanation=items["explanation"],
                    source=items["source"],
                )

                if items["product"]:
                    product = Product.objects.get_or_create(
                        name=items["product"],
                        company=company,
                    )[0]
                    rating.product = product
                else:
                    rating.company = company
                rating.save()
    calculate_total_weighted_ratings(industry)
    return True


def handle_benchmark_csv(file):
    csv_file = handle_csv(file)

    industry = None
    industry_indicators = None

    indicator_weight_total = 0

    for row in csv_file:
        if settings.DEBUG:
            print "Processing line: %d" % csv_file.line_num

        # If this is the first line, it's the industry name
        if csv_file.line_num == 1:
            industry_name = row[0]
            industry = Industry.objects.get_or_create(name=industry_name)[0]
            industry_indicators = industry.indicator_set

        else:
            if row[0] != "":
                category = IndicatorCategory.objects.get_or_create(name=row[2])[0]

                try:
                    industry_indicator = industry_indicators.get(name=row[0], category=category)
                except Indicator.DoesNotExist:
                    industry_indicator = Indicator.objects.create(
                        name=row[0],
                        category=category,
                        weight=row[1],
                        industry=industry,
                    )
                indicator_weight_total += int(row[1])

                indicator_rating_options = []
                for x in range(3,len(row)):
                    if row[x] != "":
                        indicator_rating_options.append(
                            IndicatorRatingOption.objects.create(
                                indicator=industry_indicator,
                                description=row[x],
                            )
                        )

                for x in range(0, len(indicator_rating_options)):
                    option = indicator_rating_options[x]
                    if(x == 0):
                        option.value = 1
                    elif(x == len(indicator_rating_options) - 1):
                        option.value = int(option.indicator.weight)
                    else:
                        option.value = (float(option.indicator.weight) / float(len(indicator_rating_options) - 1)) * float(x)
                    option.save()
        industry.total_weight = indicator_weight_total
        calculate_total_weighted_ratings(industry)
        industry.save()
    return True

def calculate_total_weighted_ratings(industry):
    companies = industry.company_set.select_related().all()

    for company in companies:
        total_rating = float(0)

        if company.parent:
            total_rating = Rating.objects.filter(
                company__in=[company, company.parent],
                rating__indicator__industry=industry,
            ).distinct().aggregate(v=Sum('rating__value'))['v']

            company.total_weighted_rating = total_rating / float(industry.total_weight) * 10
        else:
            total_rating = Rating.objects.filter(company=company).aggregate(v=Sum('rating__value'))['v']

        company.total_weighted_rating = total_rating / float(industry.total_weight) * 10
        company.save()

@login_required
def benchmark_input(request, template="research/benchmarks.html"):
    if request.method == "POST":
        if request.POST.get('f', None) == "benchmark":
            benchmark_form = BenchmarkCSVForm(request.POST, request.FILES)

            if benchmark_form.is_valid():
                handle_benchmark_csv(request.FILES['csv'])
                return render_to_response(template, {
                    'benchmark_success': True,
                    'benchmark_form': BenchmarkCSVForm(),
                    'research_form': ResearchCSVForm(),
                }, context_instance=RequestContext(request))
        elif request.POST.get('f', None) == "research":
            research_form = ResearchCSVForm(request.POST, request.FILES)

            if research_form.is_valid():
                handle_research_csv(request.FILES['csv'])
                return render_to_response(template, {
                    'research_success': True,
                    'benchmark_form': BenchmarkCSVForm(),
                    'research_form': ResearchCSVForm(),
                }, context_instance=RequestContext(request))
    else:
        benchmark_form = BenchmarkCSVForm()
        research_form = ResearchCSVForm()

    return render_to_response(template, {
        'benchmark_form': benchmark_form,
        'research_form': research_form,
    }, context_instance=RequestContext(request))

@login_required
def rating_output(request, template="research/print_benchmarks.html"):
    if request.method == "POST":
        form = IndustryForm(request.POST)

        if form.is_valid():
            industry = Industry.objects.get(pk=request.POST.get('select', None))

            return render_to_response(template, {
                'form': form,
                'companies': industry.company_set.select_related().all().order_by('name'),
            }, context_instance=RequestContext(request))
    else:
        form = IndustryForm()

    return render_to_response(template, {
        'form': form,
    }, context_instance=RequestContext(request))
