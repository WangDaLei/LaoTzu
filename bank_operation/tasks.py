# coding=utf-8
import os
from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from .controllers import get_reverse_repo, get_mlf, send_email
from datetime import timedelta, datetime, date

@periodic_task(run_every=crontab(hour=2, minute=5))
# @periodic_task(run_every=timedelta(minutes=1))
# Todo time is before 8 hours than actual time.
def crawl_bank_info():
    os.system('cd bank_spider && scrapy crawl url_spider')
    os.system('cd bank_spider && scrapy crawl operation_spider')
    os.system('cd bank_spider && scrapy crawl url_spider')
    os.system('cd bank_spider && scrapy crawl operation_spider')
    os.system('cd bank_spider && scrapy crawl url_spider')
    os.system('cd bank_spider && scrapy crawl operation_spider')

@periodic_task(run_every=crontab(hour=2, minute=10))
# @periodic_task(run_every=timedelta(minutes=1))
def analysis_and_send_email():
    today = date.today()
    rerepo_str = get_reverse_repo(today)
    mlf_str = get_mlf(today)
    send_email(rerepo_str + mlf_str)
