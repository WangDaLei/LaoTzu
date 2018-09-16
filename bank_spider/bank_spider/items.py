# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from bank_operation.models import OpenMarkOperationUrl, OpenMarkOperationMLF, OpenMarkOperationReverseRepo

class OpenMarkOperationUrlItem(DjangoItem):
	django_model = OpenMarkOperationUrl

class OpenMarkOperationMLFItem(DjangoItem):
	django_model = OpenMarkOperationMLF

class OpenMarkOperationReverseRepoItem(DjangoItem):
	django_model = OpenMarkOperationReverseRepo
