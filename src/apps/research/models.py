from django.db import models


"""
BENCHMARKS
"""
class IndicatorCategory(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)

class Industry(models.Model):
    name = models.CharField(max_length=200)
    total_weight = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Industries'

class Indicator(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(IndicatorCategory)
    weight = models.IntegerField()
    industry = models.ForeignKey(Industry)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ('name',)

class IndicatorRatingOption(models.Model):
    indicator = models.ForeignKey(Indicator)
    description = models.TextField()
    value = models.FloatField(null=True)

    def __unicode__(self):
        return self.description

"""
RESEARCH
"""
class Company(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey("self", blank=True, null=True)
    total_weighted_rating = models.FloatField(null=True)
    industry = models.ManyToManyField(Industry)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class Product(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name

class Rating(models.Model):
    product = models.ForeignKey(Product, null=True)
    company = models.ForeignKey(Company, null=True)
    rating = models.ForeignKey(IndicatorRatingOption)
    explanation = models.TextField()
    source = models.TextField(null=True)
    value = models.IntegerField(null=True)
