from django import forms

from apps.research.models import Industry
from apps.research.models import *


class CSVForm(forms.Form):
    csv = forms.FileField()

class BenchmarkCSVForm(CSVForm):
    f = forms.CharField(widget=forms.HiddenInput(), initial="benchmark")

class ResearchCSVForm(CSVForm):
    f = forms.CharField(widget=forms.HiddenInput(), initial="research")

class IndustryForm(forms.Form):
    select = forms.ModelChoiceField(queryset=Industry.objects.all())

"""
    def __init__(self, *args, **kwargs):
        super(IndustryForm, self ).__init__(*args,**kwargs)

        industry_choices = []

        industries = Industry.objects.all()
        for industry in industries:
            industry_choices.append((industry.name, industry.name))
"""

"""
class IndustryForm(forms.Form):
    industry = CharField(max_length=200)

class IndicatorForm(forms.Form):
    indicator = CharField(max_length=200)
    weight = IntegerField()
    category = CharField(max_length=200)

class RatingForm(forms.Form):
    rating = CharField(max_length=200)
"""
