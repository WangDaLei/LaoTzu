import datetime
import smtplib
import mistune
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from dateutil.relativedelta import relativedelta
from bank.config import mail_hostname, mail_username, mail_password, mail_encoding,\
			mail_from, mail_to
from .models import  OpenMarkOperationReverseRepo, OpenMarkOperationMLF


def add_day(date, num):
    return date + datetime.timedelta(days = num)

def add_month(date, num):
    year_num = num // 12
    month_num = num % 12
    return date + relativedelta(months = month_num) + relativedelta(years = num)

def add_year(date,num):
    return date + relativedelta(years = num)

def check_date_equal(date, last_date, num, unit):
    if unit == '天':
        return date == add_day(last_date, num)
    elif unit == '月':
        return date == add_month(last_date, num)
    elif unit == '年':
        return date == add_year(last_date, num)
    else:
        return False

def check_date_gt(date, last_date, num, unit):
    if unit == '天':
        return date < add_day(last_date, num)
    elif unit == '月':
        return date < add_month(last_date, num)
    elif unit == '年':
        return date < add_year(last_date, num)
    else:
        return False

def get_reverse_repo(date):
    reverse_repo_operation = OpenMarkOperationReverseRepo.objects\
                                        .filter(date = date)\
                                        .order_by("money")
    str_repo = ""
    if reverse_repo_operation:
        for one in reverse_repo_operation:
            str_repo += "金额:" + str(one.money) +"亿 利率:"\
                        + str(one.intereset) + "% 期限:"\
                        + str(one.duration)\
                        + str(one.duration_unit) + "\n"
    if str_repo != "":
        str_repo = "## 逆回购今日操作:\n" + "```\n" + str_repo + "```\n"

    reverse_repo_deadline = OpenMarkOperationReverseRepo.objects\
                                        .filter(date__lt=date)\
                                        .order_by("date")
    str_repo_deadline = ""
    if reverse_repo_deadline:
        for one in reverse_repo_deadline:
            if check_date_equal(date, one.date, one.duration, one.duration_unit):
                str_repo_deadline += "操作日期:" + str(one.date)\
                            + " 金额:" + str(one.money) +"亿 利率:"\
                            + str(one.intereset) + "% 期限:"\
                            + str(one.duration)\
                            + str(one.duration_unit) + "\n"

    if str_repo_deadline != "":
        str_repo_deadline = "## 逆回购今日到期:\n" + "```\n" + str_repo_deadline + "```\n"

    reverse_repo_gt = OpenMarkOperationReverseRepo.objects\
                                        .filter(date__lt=date)\
                                        .order_by("date")
    str_repo_gt = ""
    if reverse_repo_gt:
        for one in reverse_repo_gt:
            if check_date_gt(date, one.date, one.duration, one.duration_unit):
                str_repo_gt += "操作日期:" + str(one.date)\
                            + " 金额:" + str(one.money) +"亿 利率:"\
                            + str(one.intereset) + "% 期限:"\
                            + str(one.duration)\
                            + str(one.duration_unit) + "\n"

    if str_repo_gt != "":
        str_repo_gt = "## 逆回购有效操作:\n" + "```\n" + str_repo_gt + "```\n"

    return str_repo + str_repo_deadline + str_repo_gt

def get_mlf(date):
    mlf_operation = OpenMarkOperationMLF.objects\
                                        .filter(date = date)\
                                        .order_by("money")
    str_mlf = ""
    if mlf_operation:
        for one in mlf_operation:
            str_mlf += "金额:" + str(one.money) +"亿 年利率:"\
                        + str(one.intereset) + "% 期限:"\
                        + str(one.duration)\
                        + str(one.duration_unit) + "\n"
    if str_mlf != "":
        str_mlf = "## MLF今日操作:\n" + "```\n" + str_mlf + "```\n"

    mlf_deadline = OpenMarkOperationMLF.objects\
                                        .filter(date__lt=date)\
                                        .order_by("date")
    str_mlf_deadline = ""
    str_mlf_gt = ""
    if mlf_deadline:
        for one in mlf_deadline:
            if check_date_equal(date, one.date, one.duration, one.duration_unit):
                str_mlf_deadline += "操作日期:" + str(one.date)\
                            + " 金额:" + str(one.money) +"亿 利率:"\
                            + str(one.intereset) + "% 期限:"\
                            + str(one.duration)\
                            + str(one.duration_unit) + "\n"
            if check_date_gt(date, one.date, one.duration, one.duration_unit):
                str_mlf_gt += "操作日期:" + str(one.date)\
                            + " 金额:" + str(one.money) +"亿 利率:"\
                            + str(one.intereset) + "% 期限:"\
                            + str(one.duration)\
                            + str(one.duration_unit) + "\n"

    if str_mlf_deadline != "":
        str_mlf_deadline = "## MLF今日到期:\n" + "```\n" + str_mlf_deadline + "```\n"
    if str_mlf_gt != "":
        str_mlf_gt = "## MLF有效操作:\n" + "```\n" + str_mlf_gt + "```\n"

    return str_mlf + str_mlf_deadline + str_mlf_gt

def send_email(info):

    info = mistune.markdown(info, escape=True, hard_wrap=True)

    mail_info = {
        "hostname": mail_hostname,
        "username": mail_username,
        "password": mail_password,
        "mail_encoding": mail_encoding
    }

    mail_info["from"] = mail_from
    mail_info["to"] = mail_to
    mail_info["mail_subject"] = "央行今日操作和统计"
    mail_info["mail_text"] = info

    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])

    msg = MIMEText(mail_info["mail_text"], "html", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["from"] = mail_info["from"]
    msg["to"] = ",".join(mail_info["to"])

    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
    smtp.quit()
