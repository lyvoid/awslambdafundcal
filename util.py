# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime, timedelta, timezone, date
import smtplib
from email.mime.text import MIMEText
import os
import logging

tz_utc_8 = timezone(timedelta(hours=8))

msg_from = os.environ['msg_from']
email_pswd = os.environ['email_pswd']


def get_today_date():
    """
    get today date use beijing time
    :return: date with zone info(beijing)
    """
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(tz_utc_8).date()
    return bj_dt


def get_next_n_date(today, n):
    return today + timedelta(days=n)


def get_yest_date(today):
    return get_next_n_date(today, -1)


def get_tomorrow_date(today):
    return get_next_n_date(today, 1)


def get_date_by_str(date_str):
    pattern = r"^(\d+)-(\d+)-(\d+)$"
    m = re.match(pattern, date_str)
    if m is None:
        return None
    else:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def get_yest_sz_index():
    """
    :return: 这里其实拿的是当前的价格，但由于网易的api更新太慢，因此再每日的上午开市前，
    这都代表是前一天的价格
    """
    r = requests.get("http://api.money.126.net/data/feed/0000001")
    return float(re.search(r"price.*? (\d+?\.\d+?),", r.text).group(1))


def send_email(to_email, subject, content):
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = to_email
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, email_pswd)
        s.sendmail(msg_from, to_email, msg.as_string())
        logging.info('send email to %s succeed' % to_email)
    except:
        logging.info('send email to %s failed' % to_email)
    finally:
        s.quit()
