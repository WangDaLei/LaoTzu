from django.db import models

# Create your models here.
class OpenMarkOperationUrl(models.Model):
    url = models.URLField(max_length=250)
    processed = models.BooleanField(default=False)
    generated_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'bank_operation'
        # db_table = 'test_scrapy'

class OpenMarkOperationMLF(models.Model):
    STATUS_CHOICES = (
        ('天', u'天'),
        ('月', u'月'),
        ('年', u'年')
    )
    date = models.DateField()
    order = models.IntegerField()
    money = models.IntegerField()
    intereset = models.FloatField()
    duration = models.IntegerField()
    duration_unit = models.CharField(choices=STATUS_CHOICES, default='天', max_length=10)
    
    class Meta:
        app_label = 'bank_operation'
        # db_table = 'test_scrapy'

class OpenMarkOperationReverseRepo(models.Model):
    STATUS_CHOICES = (
        ('天', u'天'),
        ('月', u'月'),
        ('年', u'年')
    )
    date = models.DateField()
    order = models.IntegerField()
    money = models.IntegerField()
    intereset = models.FloatField()
    duration = models.IntegerField()
    duration_unit = models.CharField(choices=STATUS_CHOICES, default='天', max_length=10)
    
    class Meta:
        app_label = 'bank_operation'
        # db_table = 'test_scrapy'
